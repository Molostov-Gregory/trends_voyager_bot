using CSV_import.Data;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DbSqliteLibrary;

namespace CSV_import
{
    internal class TrendOperator
    {

        private List<string> wordsExeption = new List<string>()
        {
            "Категория: "
        };


        private void Extract(List<string> textLines)
        {
            var text = new List<string>();
            foreach (string wordExeption in wordsExeption)
            {
                foreach (string line in textLines)
                {
                    if (line.IndexOf(wordExeption) == -1)
                    {
                        text.Add(line);
                    }
                }
            }
            //PrintList(GetTop(text));
            Console.WriteLine("---");
            //PrintList(GetRising(text));

        }

        /// <summary>
        /// Извлекаем список данных по топу запросов
        /// </summary>
        /// <param name="textLines"></param>
        /// <returns></returns>
        public List<string> GetTop(List<string> textLines)
        {
            var topList = new List<string>();
            int indexStart = textLines.Count + 1;
            int indexFinish = textLines.Count + 1;
            for (int i = 0; i < textLines.Count; i++)
            {
                if (textLines[i].ToUpper().IndexOf("TOP") > -1)
                {
                    indexStart = i;
                }
                if (textLines[i].ToUpper().IndexOf("RISING") > -1)
                {
                    indexFinish = i;
                }
                if (i > indexStart & i < indexFinish)
                {
                    var l = textLines[i].Trim();
                    if (l.Length != 0)
                        topList.Add(textLines[i]);
                }
            }
            return topList;
        }

        /// <summary>
        /// Извлекаем список данных по топу самых трендовых запросов
        /// </summary>
        /// <param name="textLines"></param>
        /// <returns></returns>
        public List<string> GetRising(List<string> textLines)
        {
            var risingList = new List<string>();
            int indexStart = textLines.Count + 1;
            int indexFinish = textLines.Count + 1;
            for (int i = 0; i < textLines.Count; i++)
            {
                if (textLines[i].ToUpper().IndexOf("RISING") > -1)
                {
                    indexStart = i;
                }
                if (i > indexStart & i < indexFinish)
                {
                    var l = textLines[i].Trim();
                    if (l.Length != 0)
                        risingList.Add(textLines[i]);
                }
            }
            return risingList;
        }

        public List<string> GetSorterTypesSearch(List<string> patchs, string key)
        {
            var resultList = new List<string>();

            foreach (var patch in patchs)
            {
                var rows = CsvManager.CsvManager.GetCsvRow(patch);
                if (key.IndexOf(TypeSearch.top.ToString()) > -1)
                {
                    resultList.AddRange(GetTop(rows));
                }
                else if (key.IndexOf(TypeSearch.rising.ToString()) > -1)
                {
                    resultList.AddRange(GetRising(rows));
                }

            }
            return resultList;
        }

        //public 

        public void PrintList(List<string> list)
        {
            foreach (var word in list)
            {
                Console.WriteLine(word);
            }
        }


    }
}
