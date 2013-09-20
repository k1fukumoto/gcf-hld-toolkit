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
$INSTALL_DIR = Split-path (Split-path $script:MyInvocation.MyCommand.Path)
$SCRIPT_NAME = Split-path -Leaf $script:MyInvocation.MyCommand.Path
$SCRIPT_BASENAME = [System.IO.Path]::GetFileNameWithoutExtension($SCRIPT_NAME)

# Log File Location
$LOG = "$INSTALL_DIR\log\$SCRIPT_BASENAME.log"
# Log size limit in KB. Log will be renamed once size reaches this number
$LOGMAX = 1024 # KB

# $GCF_MANIFEST = "$INSTALL_DIR\config\GCF-Manifest.json"
$GCF_MANIFEST = "z:\fukumk\Desktop\Hawks\3.2\GCF-Manifest.json"

# Tool configuration
$CFG = "$INSTALL_DIR\config\config.xml"
# Credential stores
$VC_PASS = "$INSTALL_DIR\config\.vcpass.crd"

# Logging facility
function INFO ($s) {
	$l = "$(Get-Date) INFO: {0}" -f $s
	Write-Host $l -ForegroundColor Gray
	$l | Out-File $LOG -Append -Encoding ASCII
}
function ERROR ($s) {
	$l = "$(Get-Date) ERROR: {0}" -f $s
	Write-Host $l -ForegroundColor Red
	$l | Out-File $LOG -Append -Encoding ASCII
}
