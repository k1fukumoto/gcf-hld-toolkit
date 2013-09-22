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
$cred = New-Object System.Management.Automation.PSCredential($acct.vcenter.user, (Get-Content $VC_PASS | ConvertTo-SecureString))

$jso = Get-Content $GCF_VMS | Out-String | ConvertFrom-Json
$jso.psobject.properties | % {
	$region = $_.Name
	
	$vcener = ''
	if($region -eq "TOKYO") {
		$vcenter = '10.1.1.50'
	} elseif($region -eq "OSAKA") {
		$vcenter = '10.1.8.50'
	} else {
		ERROR("Unknown region {0}" -f $region)
	}
	$vc = Connect-VIServer -Server $vcenter -Credential $cred
	$_.Value.psobject.properties | % {
		$appid = $_.Name
		$vmname = $_.Value.VM

		$vm = Get-VM $vmname
		if($vm) {
			INFO("{0}: '{1}'" -f $appid, $vmname)
		} else {
			ERROR("{0}: VM '{1}' not found" -f $appid,$vmname)
		}
	}
}