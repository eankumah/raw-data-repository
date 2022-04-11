import csv
from typing import List

from google.cloud.storage.blob import Blob

from rdr_service.storage import GoogleCloudStorageFile, GoogleCloudStorageProvider
from rdr_service.tools.tool_libs.tool_base import cli_run, ToolBase, logger


tool_cmd = 'sir'
tool_desc = 'gather data from the SIRs'


class SirProcessing(ToolBase):
    def run(self):
        sir_blobs = self.get_file_list()
        sir_blobs.sort(key=lambda blob: blob.name)

        non_prep_samples = set()
        only_prep_samples = set()
        transient_prep_samples = set()

        for blob in sir_blobs:
            logger.info(blob.name)

            reader = csv.DictReader(
                GoogleCloudStorageFile(provider=GoogleCloudStorageProvider(), blob=blob),
                delimiter='\t'
            )
            sample_ids_from_file = set()

            for row in reader:
                sample_id = int(row['Sample Id'])
                storage_status = row['Sample Storage Status'].lower()
                disposal_status = row["Sample Disposal Status"].lower()

                if sample_id is None or storage_status is None:
                    raise Exception(f'Sample id or storage status missing in {blob.name}')

                sample_ids_from_file.add(sample_id)
                if sample_id in only_prep_samples:
                    raise Exception(f'found {sample_id} again in {blob.name}')

                is_in_prep = storage_status == 'in prep'
                if is_in_prep:
                    transient_prep_samples.add(sample_id)
                elif not is_in_prep:
                    if sample_id in transient_prep_samples:
                        if (storage_status, disposal_status) not in [
                            ('disposed', 'consumed'),
                            ('in circulation', '')
                        ]:
                            logger.warning(
                                f'marking {sample_id} as clean: "{storage_status}" "{disposal_status}"'
                            )
                        transient_prep_samples.remove(sample_id)
                    non_prep_samples.add(sample_id)

            # Any sample ids that are transient, but not found in the file should be marked as only_prep
            to_be_removed_from_transient = set()
            for id_ in transient_prep_samples:
                if id_ not in sample_ids_from_file:
                    only_prep_samples.add(id_)
                    to_be_removed_from_transient.add(id_)
            transient_prep_samples = {
                id_ for id_ in transient_prep_samples 
                if id_ not in to_be_removed_from_transient
            }

        with open('only_prep_output.csv', 'w') as file:
            for sample_id in only_prep_samples:
                file.write(f'{sample_id}\n')



    @classmethod
    def get_file_list(cls) -> List[Blob]:
        storage_provider = GoogleCloudStorageProvider()
        blob_list = storage_provider.list(
            bucket_name='prod_biobank_samples_upload_bucket',
            prefix='Sample Inventory Report v120'
        )

        return list(blob_list)


def run():
    return cli_run(tool_cmd, tool_desc, SirProcessing)
