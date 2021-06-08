$files = @{}
Get-ChildItem | % { 
    $files[$_.basename] = Import-Csv $_.name -Header c, guid, latency | select-object -First 1000 
}

$fmtr = ""
for ($i = 1; $i -lt $files.keys.count; $i++) {
    $t = $i - 1
    $fmtr += "{$t},"
}

write-host $fmtr

for($i = 0; $i -le 999; $i++) {
    $fmtr -f $files['sub0'].latency[$i], `
             $files['sub1'].latency[$i], `
             $files['sub2'].latency[$i], `
             $files['sub3'].latency[$i], `
             $files['sub4'].latency[$i], `
             $files['sub5'].latency[$i], `
             $files['sub6'].latency[$i], `
             $files['sub7'].latency[$i] | Out-File all_data.csv -Append -Encoding ascii
}
