using CSV_import.Data;
using Microsoft.VisualBasic;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSV_import.CsvManager
{
    public class CsvManager
    {
        private string rootPath = string.Empty;
        public CsvManager(string rootPath) { this.rootPath = rootPath; }

        public List<string> GetFilesCsv()
        {
            var list = new List<string>();
            try
            {
                // Set a variable to the My Documents path.
                string docPath = Path.Combine(rootPath);

                var files = from file in Directory.EnumerateFiles(docPath, "*.csv", SearchOption.AllDirectories)
                                //from line in File.ReadLines(file)
                                //where line.Contains("Microsoft")
                            select new
                            {
                                File = file
                            };

                foreach (var f in files)
                {
                    list.Add(f.File);
                    //Console.WriteLine($"{f.File}");
                }
                //Console.WriteLine($"{files.Count().ToString()} files found.");
            }
            catch (UnauthorizedAccessException uAEx)
            {
                Console.WriteLine(uAEx.Message);
            }
            catch (PathTooLongException pathEx)
            {
                Console.WriteLine(pathEx.Message);
            }

            return list;
        }

        public static List<string> GetSortFilesCsv(string key, List<string> list)
        {
            List<string> list2 = new List<string>();
            foreach (var item in list)
            {
                var tempKey = key.ToLower();
                var tempItem = item.ToLower();
                int tempIndex = tempItem.IndexOf(tempKey);
                if (tempIndex > -1)
                {
                    list2.Add(item);
                }
            }
            return list2;
        }

        public static List<string> GetSortFilesCsv(List<string> list, params string[] keys)
        {
            
            foreach (var key in keys)
            {
                list = GetSortFilesCsv(key, list);
            }
            return list;
        }

        public static List<string> GetCsvRow(string path)
        {
            var textLine = new List<string>();
            using (StreamReader reader = new StreamReader(path))
            {
                string? line;
                while ((line = reader.ReadLine()) != null)
                {
                    textLine.Add(line);
                }
            }
            return textLine;
        }

        public static List<string> GetCsvRow(List<string> paths)
        {
            var textLines = new List<string>();
            foreach(var path in paths)
            {
                textLines.AddRange(GetCsvRow(path));
            }
            return textLines;
        }

    }

}
