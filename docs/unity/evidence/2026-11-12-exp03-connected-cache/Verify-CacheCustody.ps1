param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$ConnectedRoot
)
$ErrorActionPreference = 'Stop'
foreach ($name in 'Core','Persistence','LabModel') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$store = [Decennium.Foundation.FileSaveStore]::new()
$before = $store.Load((Join-Path $ConnectedRoot 'csharp/before-pick.ddsave'))
$after = $store.Load((Join-Path $ConnectedRoot 'csharp/continued.ddsave'))
$hero = 'TEST_ONLY.actor'
$cache = 'TEST_ONLY.supply-cache'
$ration = 'TEST_ONLY.ready-rations'
$skin = 'TEST_ONLY.actor-skin'
$quantity = [Decennium.Foundation.RuleQuantity]::new(2)
$beforeRoot = $before.InventoryLots | Where-Object LotId -eq $ration
$afterRoot = $after.InventoryLots | Where-Object LotId -eq $ration
$child = $after.InventoryLots | Where-Object ParentId -eq $ration
$source = $before.Work.Lots | Where-Object Id -eq $ration
$depleted = $after.Work.Lots | Where-Object Id -eq $ration
$carried = $after.Work.Lots | Where-Object Id -eq $child.LotId
$beforeBurden = [Decennium.Foundation.Laboratory.TestOnlyInventoryPolicy]::CarriedBurden($before,$hero).RequireDocumentedPounds()
$afterBurden = [Decennium.Foundation.Laboratory.TestOnlyInventoryPolicy]::CarriedBurden($after,$hero).RequireDocumentedPounds()
$increase = $afterBurden - $beforeBurden
$handling = $after.Handling | Where-Object ChildId -eq $child.LotId
$beforeReserve = $before.VesselContents | Where-Object VesselId -eq $skin
$afterReserve = $after.VesselContents | Where-Object VesselId -eq $skin
$waterBefore = $before.Work.Lots | Where-Object Id -eq $beforeReserve.LotId
$waterAfter = $after.Work.Lots | Where-Object Id -eq $afterReserve.LotId
if ($source.LocationId -ne $cache -or $depleted.LocationId -ne $cache -or
    $source.Amount -ne $quantity -or $depleted.Amount.Numerator -ne 0 -or
    @($child).Count -ne 1 -or $child.OwnerId -ne $hero -or $child.Nutrition -ne 'FoodPounds' -or
    $child.CreatedAmount -ne $quantity -or $carried.Amount -ne $quantity -or $carried.UnitId -ne $source.UnitId -or
    $carried.LocationId -ne $hero -or $carried.CustodianId -ne $hero -or $handling.Kind -ne 'Pickup' -or
    $beforeRoot.CreatedAt -ne $afterRoot.CreatedAt -or $beforeRoot.FreshUntil -ne $afterRoot.FreshUntil -or
    $child.FreshUntil -ne $beforeRoot.FreshUntil -or $increase -ne $quantity -or
    $beforeReserve.LotId -ne $afterReserve.LotId -or $waterBefore.Amount -ne $waterAfter.Amount -or
    $waterBefore.LocationId -ne $skin -or $waterAfter.LocationId -ne $skin -or
    ($after.Vessels | Where-Object Id -eq $skin).LocationId -ne $hero) {
    throw 'The retained cache witness violates physical custody, freshness, mass or reserve water.'
}
[ordered]@{
    Status='PASS'; InputRevision=$before.Revision; FinalRevision=$after.Revision
    Root=$ration; RootPounds=$depleted.Amount.ToString(); Child=$child.LotId
    ChildPounds=$carried.Amount.ToString(); Unit=$carried.UnitId; ChildOwner=$child.OwnerId; ChildCustodian=$carried.CustodianId
    FreshUntil=$child.FreshUntil.ToString(); Handling=$handling.Kind.ToString()
    CarriedBeforePounds=$beforeBurden.ToString(); CarriedAfterPounds=$afterBurden.ToString(); IncreasePounds=$increase.ToString()
    CarriedVessel=$skin; ReserveLot=$afterReserve.LotId; ReservePints=$waterAfter.Amount.ToString()
} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ConnectedRoot 'custody.json') -Encoding utf8
Get-Content -LiteralPath (Join-Path $ConnectedRoot 'custody.json')
