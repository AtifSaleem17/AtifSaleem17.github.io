using IoTHubTrigger = Microsoft.Azure.WebJobs.EventHubTriggerAttribute;
using Microsoft.Azure.EventHubs;
using System.Text;
using System.Net.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using System.Collections.Generic;
using Newtonsoft.Json;
using System.Linq;

namespace http_home.monitoring
{
    // classes in which data is stored in order to display it to webApp
    public class Sensors
    {
        [JsonProperty("id")]
        public string Id{get;set;}
        public energySensor energySensorData{get;set;}
        public gasSensor gasSensorData{get;set;}
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
    public class HttpTrigger
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

        [FunctionName("getEnergyData")]
        public static IActionResult getEnergyData(
            [HttpTrigger(AuthorizationLevel.Anonymous,"get",Route ="energysensor")] HttpRequest req,
            [CosmosDB(databaseName:"homeMonitoring",collectionName:"sensorsData",
            ConnectionStringSetting="cosmosDbConnectionString",
            SqlQuery ="select * from c")] IEnumerable<Sensors> sensors,
            ILogger log )
        {
            //creating list of energy sensor data
            var energy_sensor_data=sensors.Select(x=>x.energySensorData).ToList();
            // foreach(var x in energy_sensor_data)
            // {
            //     log.LogInformation($"C# Energy List: {x.Amperes}");
            // }
            return new OkObjectResult(energy_sensor_data);
        }

        [FunctionName("getGasData")]
        public static IActionResult getGasData(
            [HttpTrigger(AuthorizationLevel.Anonymous,"get",Route ="gassensor")] HttpRequest req,
            [CosmosDB(databaseName:"homeMonitoring",collectionName:"sensorsData",
            ConnectionStringSetting="CosmosDbConnectionString",
            SqlQuery ="select * from c")] IEnumerable<Sensors> sensors,
            ILogger log )
        {        
            //creating list of gas sensor data
            var gas_sensor_data=sensors.Select(x=>x.gasSensorData).ToList();
            return new OkObjectResult(gas_sensor_data);
        }
    }
}
