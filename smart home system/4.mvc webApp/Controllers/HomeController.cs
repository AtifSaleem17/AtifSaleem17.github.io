using Newtonsoft.Json;
using Microsoft.AspNetCore.Mvc;
namespace mvc_webApp.Controllers;
public class HomeController : Controller
{
        private static string energySensorUri= "http://localhost:7071/api/energysensor";
        private static string gasSensorUri= "http://localhost:7071/api/gassensor";
        public  async Task<ActionResult> Index()
        {
            using (HttpClient client = new HttpClient())
            {
                //Initiatting the Get Request for energy sensor.
                HttpResponseMessage energySensorResponse = await client.GetAsync(energySensorUri);
                //Get the content from the response.
                HttpContent energyContent = energySensorResponse.Content;
                //Assign your content to data variable, by converting into a string using the await keyword.
                var energyResponseAsString = await energyContent.ReadAsStringAsync();
                //deserialize json object.       
                var energyResponseAsConcreteType = JsonConvert.DeserializeObject<dynamic>(energyResponseAsString);
                //Assign to viewbag object. 
                ViewBag.energySensorData = energyResponseAsConcreteType;
          
                //Initiatting the Get Request for gas sensor.
                using (HttpResponseMessage gasSensorResponse = await client.GetAsync(gasSensorUri))
                {
                    //Get the content from the response.
                    using (HttpContent gasContent = gasSensorResponse.Content)
                    {
                        //Assign your content to data variable, by converting into a string using the await keyword.
                        var gasResponseAsString = await gasContent.ReadAsStringAsync();
                        //deserialize json object.  
                        var gasResponseAsConcreteType = JsonConvert.DeserializeObject<dynamic>(gasResponseAsString);
                        //Assign to viewbag object. 
                        ViewBag.gasSensorData = gasResponseAsConcreteType;      
                    }
                }           
            }
            return View();
        }
}
