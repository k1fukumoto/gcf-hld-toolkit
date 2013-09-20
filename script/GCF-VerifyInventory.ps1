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
$vc = Connect-VIServer -Server $acct.vcenter.hostname -Credential $cred

$jso = Get-Content $GCF_MANIFEST | Out-String | ConvertFrom-Json
$jso.psobject.properties | % {
	$pod = $_.Name
	$_.Value.psobject.properties | % {
		$dc = $_.Name
		$_.Value.psobject.properties | % {
			$vb = $_.Name
			$_.Value.psobject.properties | % {
				$cluster = $_.Name
				$_.Value.psobject.properties | % {
					$appid = $_.Name
					"/$pod/$dc/$vb/$cluster/$appid"
					$_.Value.VM
					
				}
			}
		}
	}	
}