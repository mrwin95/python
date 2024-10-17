import boto3
from botocore.exceptions import ClientError

# Initialize the boto3 client for route53

route53_client = boto3.client('route53')

def delete_resource_record_sets(hosted_zone_id):
    """
     Delete all none-default records
    """

    try:
        record_sets = route53_client.list_resource_record_sets(HostedZoneId=hosted_zone_id)

        changes = []
        for record_set in record_sets['ResourceRecordSets']:
            if record_set['Type'] in ['NS', "SOA"]:
                continue

            changes.append({
                'Action': 'DELETE',
                'ResourceRecordSet': record_set
            })
        
        # if there are changes to apply, send the change request

        if changes:
            change_batch = {'Changes': changes}
            response = route53_client.change_resource_record_sets(
                HostedZoneId = hosted_zone_id,
                ChangeBatch = change_batch
            )

            print(f"Deleted non-default record sets: {response['ChangeInfo']['Id']}")
        else:
            print('Non non-default records found.')
    except ClientError as e:
        print(f"Error deleting record sets: {e}")
        return False;
    return True

def delete_hosted_zone(hosted_zone_id):
    """
        Delete specific hosted zone
    """

    if delete_resource_record_sets(hosted_zone_id):
        try:
            response = route53_client.delete_hosted_zone(Id=hosted_zone_id)
            print(f"Deleted hosted zone: {response['ChangeInfo']['Id']}")
        except ClientError as e:
            print(f"Error deleting hosted zone: {e}")
    else:
        print('Failed to delete hosted zone due to record deletion issues.')

    
if __name__ == "__main__":
    hosted_zone_id = 'Z033622335BZ1IKWBBL5X'
    delete_hosted_zone(hosted_zone_id)