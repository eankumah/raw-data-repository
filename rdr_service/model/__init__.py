# all BQ tables should be listed here
BQ_TABLES = [
    # (python path, class)
    ('rdr_service.model.bq_participant_summary', 'BQParticipantSummary'),
    ('rdr_service.model.bq_hpo', 'BQHPO'),
    ('rdr_service.model.bq_organization', 'BQOrganization'),
    ('rdr_service.model.bq_site', 'BQSite'),
    ('rdr_service.model.bq_code', 'BQCode'),

    # PDR Tables
    ('rdr_service.model.bq_questionnaires', 'BQPDRConsentPII'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRTheBasics'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRLifestyle'),
    ('rdr_service.model.bq_questionnaires', 'BQPDROverallHealth'),
    ('rdr_service.model.bq_questionnaires', 'BQPDREHRConsentPII'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRDVEHRSharing'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRFamilyHistory'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRHealthcareAccess'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRPersonalMedicalHistory'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRCOPEMay'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRCOPENov'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRCOPEDec'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRCOPEFeb'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRCOPEVaccine1'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRCOPEVaccine2'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRWithdrawalIntro'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRStopParticipating'),

    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRParticipantSummary'),

    ('rdr_service.model.bq_workbench_researcher', 'BQRWBResearcher'),
    ('rdr_service.model.bq_workbench_researcher', 'BQRWBInstitutionalAffiliations'),
    ('rdr_service.model.bq_workbench_workspace', 'BQRWBWorkspace'),
    ('rdr_service.model.bq_workbench_workspace', 'BQRWBWorkspaceUsers'),

    ('rdr_service.model.bq_genomics', 'BQGenomicSet'),
    ('rdr_service.model.bq_genomics', 'BQGenomicSetMember'),
    ('rdr_service.model.bq_genomics', 'BQGenomicJobRun'),
    ('rdr_service.model.bq_genomics', 'BQGenomicGCValidationMetrics'),
    ('rdr_service.model.bq_genomics', 'BQGenomicFileProcessed'),
    ('rdr_service.model.bq_genomics', 'BQGenomicManifestFile'),
    ('rdr_service.model.bq_genomics', 'BQGenomicManifestFeedback')
]

BQ_VIEWS = [
    # (python path, var)
    ('rdr_service.model.bq_participant_summary', 'BQParticipantSummaryView'),
    ('rdr_service.model.bq_hpo', 'BQHPOView'),
    ('rdr_service.model.bq_organization', 'BQOrganizationView'),
    ('rdr_service.model.bq_site', 'BQSiteView'),
    ('rdr_service.model.bq_code', 'BQCodeView'),
    # PDR Views
    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRParticipantSummaryView'),
    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRParticipantSummaryAllView'),
    # Disabling BQPDRParticipantSummaryWithdrawnView as a managed view;  is now a custom/manually managed view in BQ
    # ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRParticipantSummaryWithdrawnView'),
    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRPMView'),
    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRGenderView'),
    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRRaceView'),
    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRModuleView'),
    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRConsentView'),
    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRBioSpecView'),
    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRPatientStatuesView'),
    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRParticipantBiobankOrderView'),
    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDRParticipantBiobankSampleView'),
    ('rdr_service.model.bq_pdr_participant_summary', 'BQPDREhrReceiptView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRConsentPIIView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRTheBasicsView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRLifestyleView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDROverallHealthView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDREHRConsentPIIView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRDVEHRSharingView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRFamilyHistoryView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRHealthcareAccessView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRPersonalMedicalHistoryView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRCOPEMayView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRCOPENovView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRCOPEDecView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRCOPEFebView'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRCOPEVaccine1View'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRCOPEVaccine2View'),
    ('rdr_service.model.bq_questionnaires', 'BQPDRWithdrawalView'),

    ('rdr_service.model.bq_workbench_researcher', 'BQRWBResearcherView'),
    ('rdr_service.model.bq_workbench_researcher', 'BQRWBResearcherGenderView'),
    ('rdr_service.model.bq_workbench_researcher', 'BQRWBResearcherRaceView'),
    ('rdr_service.model.bq_workbench_researcher', 'BQRWBResearcherSexAtBirthView'),
    ('rdr_service.model.bq_workbench_researcher', 'BQRWBResearcherDegreeView'),
    ('rdr_service.model.bq_workbench_researcher', 'BQRWBInstitutionalAffiliationsView'),

    ('rdr_service.model.bq_workbench_workspace', 'BQRWBWorkspaceView'),
    ('rdr_service.model.bq_workbench_workspace', 'BQRWBWorkspaceRaceEthnicityView'),
    ('rdr_service.model.bq_workbench_workspace', 'BQRWBWorkspaceAgeView'),
    ('rdr_service.model.bq_workbench_workspace', 'BQRWBWorkspaceUsersView'),

    ('rdr_service.model.bq_genomics', 'BQGenomicSetView'),
    ('rdr_service.model.bq_genomics', 'BQGenomicSetMemberView'),
    ('rdr_service.model.bq_genomics', 'BQGenomicJobRunView'),
    ('rdr_service.model.bq_genomics', 'BQGenomicGCValidationMetricsView'),
    ('rdr_service.model.bq_genomics', 'BQGenomicFileProcessedView'),
    ('rdr_service.model.bq_genomics', 'BQGenomicManifestFileView'),
    ('rdr_service.model.bq_genomics', 'BQGenomicManifestFeedbackView')
]
