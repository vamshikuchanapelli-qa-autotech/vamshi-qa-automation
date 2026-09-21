*** Settings ***
Documentation    Shared API suite lifecycle.
Library    api_automation.api_helper.ApiHelper
Suite Setup    Initialize API Session
Suite Teardown    Close API Session

*** Keywords ***
Initialize API Session
    Create Bearer Token
    Print Master Cache
