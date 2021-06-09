

$list = New-Object System.Collections.ArrayList
get-childitem *.csv | foreach-object {
    $list.add((import-csv $_ -header num,guid,val))
}

$hdr = @()
for($i = 0; $i -lt $list.count; $i++) {
    $hdr += "sub$i"
}
$hdr = $hdr -join ","
$hdr | out-file all_data.csv -Append -encoding ascii
for($i = 0; $i -le 999; $i++) {
    $cval = @()
    foreach ($f in $list) {
        $cval += [string]$f[$i].val
    }
    $cval =  $cval -join ","
    $cval | Out-File all_data.csv -Append -Encoding ascii
}
