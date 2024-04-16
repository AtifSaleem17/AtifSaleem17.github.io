using Microsoft.Azure.Devices.Client;
using System;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json;
namespace SimulatedDevice
{
    internal class Program
    {
        private static DeviceClient sensors;
        //Mqtt protocol
        private static readonly TransportType s_transportType = TransportType.Mqtt;

        // The device connection string to authenticate the device with your IoT hub.
       private static string deviceConnectionString = "HostName=TempSensorHub.azure-devices.net;DeviceId=HomeMonitoringSensors;SharedAccessKey=gTJo5pi4OTwotPMEy8pzM583gsQlVPjFbbR+X/uQaBE=";
        private static async Task Main(string[] args)
        {
            Console.WriteLine("IoT Hub Quickstarts #1 - Simulated device.");

            // Connect to the IoT hub using the MQTT protocol
            sensors = DeviceClient.CreateFromConnectionString(deviceConnectionString, s_transportType);
         
            // Set up a condition to quit the sample
            Console.WriteLine("Press control-C to exit.");
            using var cts = new CancellationTokenSource();
            Console.CancelKeyPress += (sender, eventArgs) =>
            {
                eventArgs.Cancel = true;
                cts.Cancel();
                Console.WriteLine("Exiting...");
            };

            // Run the telemetry loop
            await SendDeviceToCloudMessagesAsync(cts.Token);

            // Disposing the DeviceClient object
            sensors.Dispose();
            Console.WriteLine("Device simulator finished.");
        }

        // Async method to send simulated telemetry
        private static async Task SendDeviceToCloudMessagesAsync(CancellationToken ct)
        {
            // Initialize telemetry values
            double minAmperes = 7;
            double minVoltages = 210;
            bool gas;
            double gasConcentration=20;
            var rand = new Random();

            while (!ct.IsCancellationRequested)
            {
                double currentAmperes = Math.Round((minAmperes + rand.NextDouble() * 15),2);
                int currentVoltages =Convert.ToInt32(Math.Round(minVoltages + rand.NextDouble() * 20));
                double currentGasConcentration = Math.Round((gasConcentration + rand.NextDouble() * 5),3);
                gas=Convert.ToBoolean(rand.Next(2));
                string gasType=(gas)? "TOXIC":"EXPLOSIVE";

                // create telemetry message
                var telemetryMessage=new 
                {
                        energydeviceid="Energy_Sensor",
                        amperes = currentAmperes,
                        voltages = currentVoltages,
                        gasdeviceid="Gas_Sensor",
                        gastype=gasType,
                        gasconcentration=currentGasConcentration
                };

                // Create JSON message
                string jsonMessage = JsonConvert.SerializeObject(telemetryMessage);

                using var sensorsMessage = new Message(Encoding.ASCII.GetBytes(jsonMessage));
                // Send the telemetry message
                await sensors.SendEventAsync(sensorsMessage);
                //display Json message on console
                Console.WriteLine($"{DateTime.Now} > Sending message: {jsonMessage}");

                await Task.Delay(3000);
            }
        }
    }
}
