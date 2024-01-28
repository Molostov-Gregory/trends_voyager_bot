// See https://aka.ms/new-console-template for more information
using CSV_import;
using CSV_import.CsvManager;
using CSV_import.Data;
using DbSqliteLibrary.Data;


// извлекаем пути 
string path0 = "resurse.txt";

// асинхронное чтение
var resursePaths = new List<string>();
using (StreamReader reader = new StreamReader(path0))
{
    string? path1;
    while ((path1 = reader.ReadLine()) != null)
    {
        Console.WriteLine(path1);
        resursePaths.Add(path1);
    }
}

var pathCsvData = resursePaths[0];
var pathSqlDb = resursePaths[1];
var sqlManager = new SqlManager(pathSqlDb);
var csvManager = new CsvManager(pathCsvData);
var trendsOperator = new TrendOperator();

// создание таблицы google_trends
string sendString =
    "CREATE TABLE google_trends(" +
    "_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " +
    "date TEXT NULL," +
    "state TEXT NULL," +
    "period_days INTEGER NULL," +
    "categories TEXT NULL," +
    "request_type TEXT NULL, " +
    "type_search TEXT NULL, " +
    "request_search TEXT NULL, " +
    "request TEXT NULL, " +
    "value INTEGER NULL)";
//sqlManager.SendCommand(sendString);

// создание таблицы import_data
sendString =
    "CREATE TABLE import_data(" +
    "_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " +
    "Date TEXT NOT NULL, " +
    "Path TEXT NOT NULL)";
//sqlManager.SendCommand(sendString);

//добавляем отсортированный файл в таблицу
//sqlManager.SendCommand($"INSERT INTO import_data (Date, Path) VALUES ('{DateTime.Now}', 'test_file')"); 

//добавляем списки, которые будем перебирать


// получаем список уже импортированных файлов с данными
var list_import_data = sqlManager.GetResultCommand("SELECT Path FROM import_data");

// получаем все файлы в репозитории
var list = csvManager.GetFilesCsv();
foreach (var file in list)
{
    if (file.IndexOf("mou") > -1)
    {
        Console.WriteLine(file);
    }
}
//sqlManager.SendCommand($"INSERT INTO import_data (Date, Path) VALUES ('{DateTime.Now}', 'C:\\Users\\ADM\\Dropbox\\Data_trend_analysis\\03-01-2024\\world\\all\\12_months\\web\\relatedQueries.csvC:\\Users\\ADM\\Dropbox\\Data_trend_analysis\\03-01-2024\\world\\all\\12_months\\web\\relatedQueries.csv')");
// отбираем лишние файлы, которые уже были обработаны
for (int i = list.Count - 1; i >= 0; i--)
{
    foreach (var item2 in list_import_data)
    {
        if (list[i].ToLower().IndexOf(item2[0].ToString().ToLower()) != -1)
        {
            list.RemoveAt(i);
            break;
        }
    }
}


// перебираем файлы и записываем их в базу данных
var startDate = new DateTime(2024, 01, 01);
var finishDate = DateTime.Now;
var currentDate = new DateTime(2024, 01, 01);
while (currentDate < finishDate)
{
    foreach (var state in TrendCategotyConst.states)
    {
        foreach (var category in TrendCategotyConst.categories)
        {
            foreach (var periodDay in TrendCategotyConst.periodDays)
            {
                foreach (var requestSearch in TrendCategotyConst.requestSearchs)
                {
                    foreach (var requestType in TrendCategotyConst.requestTypes)
                    {
                        foreach (var typeSearch in TrendCategotyConst.typesSearch)
                        {

                            var stringDate = currentDate.ToString("dd-MM-yyyy");
                            var tempStringState = state + "\u005c";
                            var listData = CsvManager.GetSortFilesCsv(list, stringDate, tempStringState, category, periodDay, requestSearch, requestType);
                            var tempList = CsvManager.GetSortFilesCsv(list, "14-01-2024", "ru\u005c", "all", "12_mouth", "web", "queries");
                            if (listData.Count == 1)
                            {
                                Console.WriteLine("");
                                foreach (var item in listData) { Console.WriteLine(item); }
                            }
                            var sorterRows = trendsOperator.GetSorterTypesSearch(listData, typeSearch);
                            if (sorterRows.Count > 0)
                            {
                                int value;
                                int intPeriodDay = 0;

                                for (int g = 0; g < sorterRows.Count; g++)
                                {
                                    string[] words;
                                    if (sorterRows[g].IndexOf("%") > -1)
                                    {
                                        //значит это проценты
                                        words = sorterRows[g].Split(",+");
                                        if (words[1].IndexOf("п") > -1)
                                        {
                                            Console.WriteLine("Test");
                                        }
                                        words[1] = words[1].Trim().Replace("%", "");
                                        var word = words[1].Replace(",", "").Replace(" ", "").Trim();

                                        for (int c = 0; c < word.Length; c++)
                                        {
                                            if ((int)word[c] == 160)
                                            {
                                                word = word.Remove(c, 1);
                                            }
                                        }
                                        if (!Int32.TryParse(word, out value))
                                        {
                                            foreach (var item in word)
                                            {
                                                Console.WriteLine((int)item);
                                            }
                                            Console.WriteLine(word + ";");
                                        }
                                        if (word.IndexOf("п") > -1)
                                        {
                                            Console.WriteLine("Test");
                                            word = word.Replace("Сверхпопулярность", "5100");
                                        }
                                        if (value >= 6000)
                                        {
                                            value += (100 + 100 / (g + 1));
                                        }
                                    }
                                    else
                                    {
                                        words = sorterRows[g].Split(",");
                                        var word = words[1].Trim().Replace(",", "").Replace(" ", "");
                                        if (word.IndexOf("п") > -1)
                                        {
                                            Console.WriteLine(words[0]);
                                            word = word.Replace("Сверхпопулярность", "5100");
                                        }
                                        if (!Int32.TryParse(word, out value))
                                        {
                                            Console.WriteLine(word + ";;");
                                        }
                                        if (value >= 5100)
                                        {
                                            value += 25 - g;
                                        }
                                    }


                                    switch (periodDay)
                                    {
                                        case "12_months":
                                            intPeriodDay = 365;
                                            break;
                                        case "90_days":
                                            intPeriodDay = 90;
                                            break;
                                        case "30_days":
                                            intPeriodDay = 30;
                                            break;
                                    }
                                    if (intPeriodDay == 0)
                                    {
                                        Console.WriteLine("!!");
                                    }

                                    var row = new Row()
                                    {
                                        Request = words[0].Replace("'", ""),
                                        Value = value
                                    };
                                    sqlManager.SendCommand($"INSERT INTO google_trends (date, state, period_days, categories, request_type, type_search, request_search, request, value) VALUES " +
                                        $"('{currentDate.ToString("dd-MM-yyyy")}', '{state}', {intPeriodDay}, '{category}', '{requestType}', '{typeSearch}', '{requestSearch}', '{row.Request}', {row.Value})");

                                }

                                var path = listData[0];
                                sqlManager.SendCommand($"INSERT INTO import_data (Date, Path) VALUES ('{DateTime.Now}', '{path}')");
                            }
                            //trendsOperator.PrintList(sorterRows);

                            //Console.WriteLine();
                            //Console.WriteLine($"typeSearch = {typeSearch}; category = {category}; periodDay = {periodDay}; requestSearch = {requestSearch}; requestType = {requestType}; state = {state}; stringDate = {stringDate}");
                            //Console.WriteLine("---");


                        }
                    }
                }
            }
        }
    }
    currentDate = currentDate.AddDays(1);
}
Console.WriteLine("---");
Console.WriteLine("End");