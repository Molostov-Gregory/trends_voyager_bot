using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DbSqliteLibrary.Data
{
    /// <summary>
    /// Структура, которую будем использовать для сортировки выборки
    /// </summary>
    public class SorterElement
    {
        public DateTime DateStart { get; set; } = new DateTime(2024, 1, 1);
        public DateTime DateFinish { get; set; } = DateTime.Now;
        public string State { get; set; }
        public int PeriodDays { get; set; }
        public string Category { get; set; }
        public string RequestType { get; set; }
        public string TypeSearch { get; set; }
        public string RequestSearch { get; set; }
    }
}
