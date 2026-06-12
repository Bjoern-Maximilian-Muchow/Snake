param(
  [string]$Port = "COM3",
  [int]$Baud = 115200
)

$serial = [System.IO.Ports.SerialPort]::new($Port, $Baud)
$serial.NewLine = "`n"
$serial.ReadTimeout = 1000

try {
  $serial.Open()
  Write-Host "AutoSnake Serial Monitor auf $Port mit $Baud Baud. Abbruch mit Ctrl+C."
  while ($true) {
    try {
      $line = $serial.ReadLine()
      Write-Host $line.TrimEnd()
    } catch [System.TimeoutException] {
    }
  }
} finally {
  if ($serial.IsOpen) {
    $serial.Close()
  }
}
