*** Settings ***
Documentation    Basic API suite sample.
Library    api_automation.api_helper.ApiHelper

*** Test Cases ***
Bearer Token Is Available
    [Documentation]    Verify suite setup created and stored an access token.
    [Tags]    smoke    priority_medium
    ${token}=    Get Master Cache Value    ACCESS_TOKEN
    Log    ACCESS_TOKEN is available in master_cache
    Should Not Be Empty    ${token}

Get Authenticated User
    [Documentation]    Verify the stored bearer token can call the auth/me endpoint.
    [Tags]    smoke    get    priority_high
    ${token}=    Get Master Cache Value    ACCESS_TOKEN
    ${user}=    Get Authenticated User    https://dummyjson.com/auth/me    ${token}
    Log    Authenticated user response received
    Should Not Be Empty    ${user}
