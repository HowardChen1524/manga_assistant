using Python.Runtime;
using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using System.IO;
using System.Xml;

class Program
{
    static void Main()
    {
        // 初始化Python運行時
        Runtime.PythonDLL = @"C:\Program Files\Python311\python311.dll";
        PythonEngine.PythonHome = @"C:\Program Files\Python311";
        PythonEngine.Initialize();

        using (Py.GIL())
        {
            // 載入Python腳本
            dynamic scraper = Py.Import("scraper");

            // 呼叫 get_info 函數並傳遞URL
            string url = "https://m.happymh.com/manga/quanzhiduzheshijiao";
            dynamic result = scraper.get_info(url);

            // 將Python defaultdict轉換為C# Dictionary<string, string>
            Dictionary<string, string> infoDict = new Dictionary<string, string>();
            foreach (dynamic key in result.keys())
            {
                infoDict[(string)key] = (string)result[key];
            }

            // 將字典序列化為JSON格式
            string json = JsonConvert.SerializeObject(infoDict, Newtonsoft.Json.Formatting.Indented);

            // 將JSON寫入文件
            string filePath = "output.json";
            File.WriteAllText(filePath, json);

            Console.WriteLine("JSON output has been written to " + filePath);
        }

        // 關閉Python運行時
        PythonEngine.Shutdown();
    }
}
