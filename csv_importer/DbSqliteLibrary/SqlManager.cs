using DbSqliteLibrary.Data;
using Microsoft.Data.Sqlite;
using Newtonsoft.Json;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Data;
using System.Data.Common;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSV_import
{
    public class SqlManager
    {
        private string dbName {  get; set; }
        private string tableName { get; set; }
        private string path { get; set; }

        private string connectionString { get; set; }
        public SqlManager(string _dbName)
        {
            //using (StreamReader r = new StreamReader("appsettings.json"))
            //{
            //    string json = r.ReadToEnd();
            //    AppsettingsClass items = JsonConvert.DeserializeObject<AppsettingsClass>(json);
            //    this.dbName = items.dbName;
            //}
            dbName = _dbName;
            this.path = "";
            connectionString = "Data Source=" + dbName + ".db";
        }

        public void SendCommand(string sqlCommand)
        {
            using (var connection = new SqliteConnection(connectionString))
            {
                connection.Open();
                SqliteCommand command = new SqliteCommand();
                command.Connection = connection;
                command.CommandText = sqlCommand;
                command.ExecuteNonQuery();
            }
        }

        public List<List<object>> GetResultCommand(string sqlCommand)
        {
            List<List<object>> result = new List<List<object>>();
            using (var connection = new SqliteConnection(connectionString))
            {
                connection.Open();
                SqliteCommand command = new SqliteCommand(sqlCommand, connection);
                using (SqliteDataReader reader = command.ExecuteReader())
                {
                    if (reader.HasRows) // если есть данные
                    {
                        while (reader.Read())   // построчно считываем данные
                        {
                            var row = new List<object>();
                            var columnSchema = reader.GetColumnSchema();
                            for(int i=0; i<columnSchema.Count; i++)
                            {
                                if (columnSchema[i].DataTypeName == "INTEGER")
                                {       
                                    var value = Convert.ToInt32(reader.GetValue(i));
                                    row.Add(value);
                                }
                                if (columnSchema[i].DataTypeName == "NUMERIC")
                                {
                                    var value = Convert.ToDouble(reader.GetValue(i));
                                    row.Add(value);
                                }
                                if (columnSchema[i].DataTypeName == "TEXT")
                                {
                                    var value = reader.GetString(i);
                                    row.Add(value);
                                }
                                if (columnSchema[i].DataTypeName == "REAL")
                                {
                                    var value = Convert.ToSingle(reader.GetValue(i));
                                    row.Add(value);
                                }
                            }
                            result.Add(row);
                            
                        }
                    }
                }
            }
            return result;
        }
    }
}
