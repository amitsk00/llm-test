from google.cloud import dlp_v2
from google.cloud.dlp_v2 import types

def redact_cvv(text_to_inspect: str):
    dlp = dlp_v2.DlpServiceClient()
    project = "your-gcp-project-id"
    parent = f"projects/{project}/locations/global"

    item = {"value": text_to_inspect}

    # Configure the inspection to look specifically for CVV
    inspect_config = {
        "info_types": [{"name": "CREDIT_CARD_CVV"}],
        "include_quote": True,
    }

    # What to do with detected info (redact)
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "info_types": [{"name": "CREDIT_CARD_CVV"}],
                    "primitive_transformation": {
                        "replace_with_info_type_config": {}
                    },
                }
            ]
        }
    }

    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "deidentify_config": deidentify_config,
            "item": item,
        }
    )

    return response.item.value

def inspect_cvv(text_to_inspect: str):
    dlp = dlp_v2.DlpServiceClient()
    project = "fraud-maplequad"
    parent = f"projects/{project}/locations/europe-west2"

    item = {"value": text_to_inspect}

    # Configure the inspection for CVV basis config created
    inspect_config = {
        "info_types": [{"name": "projects/fraud-maplequad/locations/europe-west2/inspectTemplates/nlp-cvv1"}],
        "include_quote": True,   
    }

    # Call the DLP API to inspect the text
    response = dlp.code assist(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Process and return the inspection results
    findings = response.result.findings
    if findings:
        for finding in findings:
            print(f"Info type: {finding.info_type.name}")
            print(f"Likelihood: {finding.likelihood}")
            print(f"Quote: {finding.quote}")
    else:
        print("No CVV found.")





text = "Customer CVV is 123"
redacted_text = redact_cvv(text)
print(redacted_text)

inspect_cvv(text)

