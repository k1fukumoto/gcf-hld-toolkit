#######################################################################################
# Copyright 2013 VCE All Rights Reserved
#
# You may freely use and redistribute this script as long as this 
# copyright notice remains intact 
#
#
# DISCLAIMER. THIS SCRIPT IS PROVIDED TO YOU "AS IS" WITHOUT WARRANTIES OR CONDITIONS 
# OF ANY KIND, WHETHER ORAL OR WRITTEN, EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY 
# DISCLAIMS ANY IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY 
# QUALITY, NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE. 
#
#######################################################################################
. .\config\environment.ps1

[xml]$cfg = Get-Content $CFG
$acct = $cfg.config.account
#$cred = New-Object System.Management.Automation.PSCredential($acct.vcenter.user, (Get-Content $VC_PASS | ConvertTo-SecureString))
#$vc = Connect-VIServer -Server '10.1.1.50','10.1.8.50' -Credential $cred

$jso = Get-Content $GCF_VMS | Out-String | ConvertFrom-Json
$jso.psobject.properties | % {
	$appid = $_.Name
	$vmname = $_.Value.VM

	$vm = Get-VM $vmname
	if($vm) {
		INFO("{0}: '{1}'" -f $appid, $vmname)
	} else {
		ERROR("VM {0} not found" -f $vmname)
	}
}