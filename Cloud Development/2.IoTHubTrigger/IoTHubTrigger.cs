using IoTHubTrigger = Microsoft.Azure.WebJobs.EventHubTriggerAttribute;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.EventHubs;
using System.Text;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System.Net.Http;

namespace iotHub_home.monitoring
{
    // classes in which data is stored in order to store it to cosmosDB
    public class Sensors
    {
        [JsonProperty("id")]
        public string Id{get;set;}
        public energySensor energySensorData {get; set;}
        public gasSensor gasSensorData {get; set;}
    }
    public class energySensor
    {
        public string SensorId{get;set;}
        public double Amperes{get;set;}
        public double Voltages{get;set;}
    }
    public class gasSensor
    {
        public string SensorId{get;set;}
        public string GasType{get;set;}
        public double GasConcentration{get;set;}
    }
    public class ioTHubTrigger
    {
        private static HttpClient client = new HttpClient();
        
        [FunctionName("ioTHubTrigger")]
        public void Run([IoTHubTrigger("messages/events", Connection = "IoTHubConnection")]EventData message,
         [CosmosDB(databaseName: "homeMonitoring",
                 collectionName: "sensorsData",
                 ConnectionStringSetting = "cosmosDBConnectionString")] out Sensors sensors,
                  ILogger log)
        {
            log.LogInformation($"C# IoT Hub trigger function processed a message: {Encoding.UTF8.GetString(message.Body.Array)}");
            var jsonBody = Encoding.UTF8.GetString(message.Body);
            dynamic data = JsonConvert.DeserializeObject(jsonBody);

                sensors=new Sensors
                {
                    //Energy sensor data storing
                 energySensorData=new energySensor
                 {
                    SensorId=data.energydeviceid,
                    Amperes=data.amperes,
                    Voltages=data.voltages
                 },
                 //gas sensor data storing
                 gasSensorData=new gasSensor
                 {
                    SensorId=data.gasdeviceid,
                    GasType=data.gastype,
                    GasConcentration=data.gasconcentration
                 }
              };
        }
    }
}