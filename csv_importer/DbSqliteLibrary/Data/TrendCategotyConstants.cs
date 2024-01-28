using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DbSqliteLibrary.Data
{
    public static class TrendCategotyConst
    {
        public static List<string> categories = new List<string>(){
        "all",
        "entertainment",
        "game"
        };
        public static List<string> periodDays = new List<string>(){
        "12_months",
        "30_days",
        "90_days"
        };
        public static List<string> requestSearchs = new List<string>(){
        "web",
        "youtube"
        };
        public static List<string> requestTypes = new List<string>(){
        "queries",
        "entities"
        };
        public static List<string> states = new List<string>(){
        "ru",
        "world",
        "us"
        };
        public static List<string> typesSearch = new List<string>(){
        "rising",
        "top"
        };
    }
}
