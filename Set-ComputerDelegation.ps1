function Set-ComputerDelegation() {
	param(
	[string]$ou,
	[string]$groupName
	)
    $ADRights = "GenericAll"
    $aceType = "Allow"
    # get the schemaIDGuid for the computer class
    $computerObjectGuid = new-object Guid bf967a86-0de6-11d0-a285-00aa003049e2
    $identity = New-Object System.Security.Principal.SecurityIdentifier (Get-ADGroup $groupName).SID
    $acl = get-acl $ou
    $ace = new-object System.DirectoryServices.ActiveDirectoryAccessRule $identity,$ADRights,$aceType,"All",$computerObjectGuid

    $acl.AddAccessRule($ace)
    set-acl -aclobject $acl $ou
}

$ou = "AD:\\" + "OU=lab,DC=workshop,DC=local"
$groupName = "WSFC_NAME"+ "_cluster"
Set-ComputerDelegation -ou $ou -groupName $groupName
