import os
import datetime

from rdr_service import clock, config
from rdr_service.api_util import list_blobs, delete_cloud_file
from rdr_service.offline.sql_exporter import SqlExporter
from rdr_service.dao.hpo_dao import HPODao
from rdr_service.dao.participant_summary_dao import ParticipantSummaryDao

CSV_HEADER = ['PMI ID',
              'Biobank ID',
              'Last Name',
              'First Name',
              'Middle Initial',
              'Age Range',
              'Participant Status',
              'Primary Consent Status',
              'EHR Consent Status',
              'CABoR Consent Status',
              'Withdrawal Status',
              'Deactivation Status',
              'Withdrawal Reason',
              'Street Address',
              'Street Address 2',
              'City',
              'State',
              'ZIP',
              'Email',
              'Phone',
              'Age',
              'Sex',
              'Gender Identity',
              'Race and Ethnicity',
              'Education',
              'Required PPI Surveys Complete',
              'Completed Surveys',
              'Basics PPI Survey Complete',
              'Health PPI Survey Complete',
              'Lifestyle PPI Survey Complete',
              'Med History PPI Survey Complete',
              'Family History PPI Survey Complete',
              'Access PPI Survey Complete',
              'Physical Measurements Status',
              'Paired Site',
              'Paired Organization',
              'Awardee',
              'Physical Measurements Site',
              'Samples to Isolate DNA',
              'Baseline Samples Received',
              '8 mL SST Received',
              '8 mL PST Received',
              '4 mL Na-Hep Received',
              '2 mL EDTA Received',
              '4 mL EDTA Received',
              '1st 10 mL EDTA Received',
              '2nd 10 mL EDTA Received',
              'Cell-Free DNA Received',
              'Paxgene RNA Received',
              'Urine 10 mL Received',
              'Urine 90 mL Received',
              'Saliva Received',
              'Biospecimens Site',
              'Language of Primary Consent',
              'DV-only EHR Sharing',
              'Login Phone',
              'Patient Status',
              'Participant Origination',
              'Genetic Return of Results Consent Status',
              'COPE May PPI Survey Complete',
              'COPE June PPI Survey Complete',
              'COPE July PPI Survey Complete',
              'Consent Cohort',
              'Program Update',
              'EHR Expiration Status',
              'Retention Eligible',
              'Deceased',
              'COPE Nov PPI Survey Complete',
              'Retention Status',
              'EHR Data Transfer',
              'Saliva Collection',
              'COPE Dec PPI Survey Complete',
              'COPE Feb PPI Survey Complete',
              'Summer Minute PPI Survey Complete',
              'Fall Minute PPI Survey Complete',
              'Digital Health Consent',
              'Personal & Family Hx PPI Survey Complete',
              'SDOH PPI Survey Complete',
              'Winter Minute PPI Survey Complete',
              'New Year Minute PPI Survey Complete',
              ]
DATETIME_FIELDS = ['consentForStudyEnrollmentAuthored',
                   'consentForElectronicHealthRecordsAuthored',
                   'consentForCABoRTimeAuthored',
                   'withdrawalAuthored',
                   'suspensionTime',
                   'questionnaireOnTheBasicsAuthored',
                   'questionnaireOnOverallHealthAuthored',
                   'questionnaireOnLifestyleAuthored',
                   'questionnaireOnMedicalHistoryAuthored',
                   'questionnaireOnFamilyHealthAuthored',
                   'questionnaireOnHealthcareAccessAuthored',
                   'physicalMeasurementsFinalizedTime',
                   'sampleStatus1SST8Time',
                   'sampleStatus1PST8Time',
                   'sampleStatus1HEP4Time',
                   'sampleStatus1ED02Time',
                   'sampleStatus1ED04Time',
                   'sampleStatus1ED10Time',
                   'sampleStatus2ED10Time',
                   'sampleStatus1CFD9Time',
                   'sampleStatus1PXR2Time',
                   'sampleStatus1UR10Time',
                   'sampleStatus1UR90Time',
                   'sampleStatus1SALTime',
                   'enrollmentStatusCoreStoredSampleTime',
                   'consentForGenomicsRORAuthored',
                   'questionnaireOnCopeMayTime',
                   'questionnaireOnCopeJuneTime',
                   'questionnaireOnCopeJulyAuthored',
                   'ehrconsentExpireAuthored',
                   'consentForStudyEnrollmentFirstYesAuthored',
                   'consentForElectronicHealthRecordsFirstYesAuthored',
                   'retentionEligibleTime',
                   'dateOfDeath',
                   'deceasedAuthored',
                   'questionnaireOnCopeNovAuthored',
                   'latestEhrReceiptTime',
                   'questionnaireOnCopeDecAuthored',
                   'questionnaireOnCopeFebAuthored',
                   'questionnaireOnCopeVaccineMinute1Authored',
                   'questionnaireOnCopeVaccineMinute2Authored',
                   'questionnaireOnPersonalAndFamilyHealthHistoryAuthored',
                   'questionnaireOnSocialDeterminantsOfHealthAuthored',
                   'questionnaireOnCopeVaccineMinute3Authored',
                   'questionnaireOnCopeVaccineMinute4Authored',
                   'questionnaireOnDnaProgramAuthored',
                   'enrollmentStatusCoreMinusPMTime'
                   ]
_INPUT_CSV_TIME_FORMAT_LENGTH = 18
_CSV_SUFFIX_LENGTH = 4
INPUT_CSV_TIME_FORMAT = "%Y-%m-%d-%H-%M-%S"
_MAX_FILE_AGE = datetime.timedelta(days=7)
FILE_PREFIX = 'va_daily_participant_wq_'


def _set_defaults(participant):
    for field in DATETIME_FIELDS:
        participant.setdefault(field, 'UNSET')


def generate_workqueue_report():
    """ Creates csv file from ParticipantSummary table for participants paired to VA """
    hpo_dao = HPODao()
    summary_dao = ParticipantSummaryDao()
    bucket = config.getSetting(config.VA_WORKQUEUE_BUCKET_NAME)
    subfolder = config.getSetting(config.VA_WORKQUEUE_SUBFOLDER)
    file_timestamp = clock.CLOCK.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = f'{FILE_PREFIX}{file_timestamp}.csv'
    participants = summary_dao.get_by_hpo(hpo_dao.get_by_name('VA'))
    participants_new = []
    for participant in participants:
        participant_filtered = summary_dao.to_client_json(participant, strip_none_values=False)
        _set_defaults(participant_filtered)
        participant_row = [participant_filtered["participantId"],
                           participant_filtered["biobankId"],
                           participant_filtered["lastName"],
                           participant_filtered["firstName"],
                           participant_filtered["middleName"],
                           participant_filtered["ageRange"],
                           participant_filtered["enrollmentStatus"],
                           participant_filtered["consentForStudyEnrollment"],
                           participant_filtered["consentForStudyEnrollmentAuthored"],
                           participant_filtered["consentForElectronicHealthRecords"],
                           participant_filtered["consentForElectronicHealthRecordsAuthored"],
                           participant_filtered["consentForCABoR"],
                           participant_filtered["consentForCABoRTimeAuthored"],
                           participant_filtered["withdrawalStatus"],
                           participant_filtered["withdrawalAuthored"],
                           participant_filtered["suspensionStatus"],
                           participant_filtered["suspensionTime"],
                           participant_filtered["withdrawalReason"],
                           participant_filtered["streetAddress"],
                           participant_filtered["streetAddress2"],
                           participant_filtered["city"],
                           participant_filtered["state"],
                           participant_filtered["zipCode"],
                           participant_filtered["email"],
                           participant_filtered["phoneNumber"],
                           participant_filtered["ageRange"],
                           participant_filtered["sex"],
                           participant_filtered["genderIdentity"],
                           participant_filtered["race"],
                           participant_filtered["education"],
                           participant_filtered["numCompletedBaselinePPIModules"],
                           participant_filtered["numCompletedPPIModules"],
                           participant_filtered["questionnaireOnTheBasics"],
                           participant_filtered["questionnaireOnTheBasicsAuthored"],
                           participant_filtered["questionnaireOnOverallHealth"],
                           participant_filtered["questionnaireOnOverallHealthAuthored"],
                           participant_filtered["questionnaireOnLifestyle"],
                           participant_filtered["questionnaireOnLifestyleAuthored"],
                           participant_filtered["questionnaireOnMedicalHistory"],
                           participant_filtered["questionnaireOnMedicalHistoryAuthored"],
                           participant_filtered["questionnaireOnFamilyHealth"],
                           participant_filtered["questionnaireOnFamilyHealthAuthored"],
                           participant_filtered["questionnaireOnHealthcareAccess"],
                           participant_filtered["questionnaireOnHealthcareAccessAuthored"],
                           participant_filtered["physicalMeasurementsStatus"],
                           participant_filtered["physicalMeasurementsFinalizedTime"],
                           participant_filtered["site"],
                           participant_filtered["organization"],
                           participant_filtered["awardee"],
                           participant_filtered["physicalMeasurementsFinalizedSite"],
                           participant_filtered["samplesToIsolateDNA"],
                           participant_filtered["numBaselineSamplesArrived"],
                           participant_filtered["sampleStatus1SST8"],
                           participant_filtered["sampleStatus1SST8Time"],
                           participant_filtered["sampleStatus1PST8"],
                           participant_filtered["sampleStatus1PST8Time"],
                           participant_filtered["sampleStatus1HEP4"],
                           participant_filtered["sampleStatus1HEP4Time"],
                           participant_filtered["sampleStatus1ED02"],
                           participant_filtered["sampleStatus1ED02Time"],
                           participant_filtered["sampleStatus1ED04"],
                           participant_filtered["sampleStatus1ED04Time"],
                           participant_filtered["sampleStatus1ED10"],
                           participant_filtered["sampleStatus1ED10Time"],
                           participant_filtered["sampleStatus2ED10"],
                           participant_filtered["sampleStatus2ED10Time"],
                           participant_filtered["sampleStatus1CFD9"],
                           participant_filtered["sampleStatus1CFD9Time"],
                           participant_filtered["sampleStatus1PXR2"],
                           participant_filtered["sampleStatus1PXR2Time"],
                           participant_filtered["sampleStatus1UR10"],
                           participant_filtered["sampleStatus1UR10Time"],
                           participant_filtered["sampleStatus1UR90"],
                           participant_filtered["sampleStatus1UR90Time"],
                           participant_filtered["sampleStatus1SAL"],
                           participant_filtered["sampleStatus1SALTime"],
                           participant_filtered["biospecimenSourceSite"],
                           participant_filtered["primaryLanguage"],
                           participant_filtered["consentForDvElectronicHealthRecordsSharing"],
                           participant_filtered["loginPhoneNumber"],
                           participant_filtered["patientStatus"],
                           participant_filtered["enrollmentStatusCoreStoredSampleTime"],
                           participant_filtered["participantOrigin"],
                           participant_filtered["consentForGenomicsROR"],
                           participant_filtered["consentForGenomicsRORAuthored"],
                           participant_filtered["questionnaireOnCopeMay"],
                           participant_filtered["questionnaireOnCopeMayTime"],
                           participant_filtered["questionnaireOnCopeJune"],
                           participant_filtered["questionnaireOnCopeJuneTime"],
                           participant_filtered["questionnaireOnCopeJuly"],
                           participant_filtered["questionnaireOnCopeJulyAuthored"],
                           participant_filtered["consentCohort"],
                           participant_filtered["questionnaireOnDnaProgram"],
                           participant_filtered["questionnaireOnDnaProgramAuthored"],
                           participant_filtered["ehrConsentExpireStatus"],
                           participant_filtered["ehrconsentExpireAuthored"],
                           participant_filtered["consentForStudyEnrollmentFirstYesAuthored"],
                           participant_filtered["consentForElectronicHealthRecordsFirstYesAuthored"],
                           participant_filtered["retentionEligibleStatus"],
                           participant_filtered["retentionEligibleTime"],
                           participant_filtered["deceasedStatus"],
                           participant_filtered["dateOfDeath"],
                           participant_filtered["deceasedAuthored"],
                           participant_filtered["questionnaireOnCopeNov"],
                           participant_filtered["questionnaireOnCopeNovAuthored"],
                           participant_filtered["retentionType"],
                           participant_filtered["isEhrDataAvailable"],
                           participant_filtered["latestEhrReceiptTime"],
                           participant_filtered["sample1SAL2CollectionMethod"],
                           participant_filtered["questionnaireOnCopeDec"],
                           participant_filtered["questionnaireOnCopeDecAuthored"],
                           participant_filtered["questionnaireOnCopeFeb"],
                           participant_filtered["questionnaireOnCopeFebAuthored"],
                           participant_filtered["enrollmentStatusCoreMinusPMTime"],
                           participant_filtered["questionnaireOnCopeVaccineMinute1"],
                           participant_filtered["questionnaireOnCopeVaccineMinute1Authored"],
                           participant_filtered["questionnaireOnCopeVaccineMinute2"],
                           participant_filtered["questionnaireOnCopeVaccineMinute2Authored"],
                           participant_filtered["digitalHealthSharingStatus"],
                           participant_filtered["questionnaireOnPersonalAndFamilyHealthHistory"],
                           participant_filtered["questionnaireOnPersonalAndFamilyHealthHistoryAuthored"],
                           participant_filtered["questionnaireOnSocialDeterminantsOfHealth"],
                           participant_filtered["questionnaireOnSocialDeterminantsOfHealthAuthored"],
                           participant_filtered["questionnaireOnCopeVaccineMinute3"],
                           participant_filtered["questionnaireOnCopeVaccineMinute3Authored"],
                           participant_filtered["questionnaireOnCopeVaccineMinute4"],
                           participant_filtered["questionnaireOnCopeVaccineMinute4Authored"],
                           ]
        participants_new.append(participant_row)
    exporter = SqlExporter(bucket)
    with exporter.open_cloud_writer(subfolder + "/" + file_name) as writer:
        writer.write_header(CSV_HEADER)
        writer.write_rows(participants_new)


def delete_old_reports():
    """ Deletes export files that are more than 7 days old """
    bucket = config.getSetting(config.VA_WORKQUEUE_BUCKET_NAME)
    subfolder = config.getSetting(config.VA_WORKQUEUE_SUBFOLDER)
    now = clock.CLOCK.now()
    for file in list_blobs(bucket, subfolder):
        if file.name.endswith(".csv") and os.path.basename(file.name).startswith(FILE_PREFIX):
            file_time = _timestamp_from_filename(file.name)
            if now - file_time > _MAX_FILE_AGE:
                delete_cloud_file(bucket + "/" + file.name)


def _timestamp_from_filename(csv_filename):
    if len(csv_filename) < _INPUT_CSV_TIME_FORMAT_LENGTH + _CSV_SUFFIX_LENGTH:
        raise RuntimeError("Can't parse time from CSV filename: %s" % csv_filename)
    time_suffix = csv_filename[
                  len(csv_filename)
                  - (_INPUT_CSV_TIME_FORMAT_LENGTH + _CSV_SUFFIX_LENGTH)
                  - 1: len(csv_filename)
                       - _CSV_SUFFIX_LENGTH
                  ]
    try:
        timestamp = datetime.datetime.strptime(time_suffix, INPUT_CSV_TIME_FORMAT)
    except ValueError as timestamp_parse_error:
        raise RuntimeError("Can't parse time from CSV filename: %s" % csv_filename) from timestamp_parse_error
    return timestamp
