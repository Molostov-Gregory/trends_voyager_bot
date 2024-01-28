using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSV_import.Data
{
    public class UnitTrend
    {
        public DateTime Date { get; set; }
        public string State { get; set; }
        public int PeriodDays { get; set; }
        public string Category { get; set; }
        public string RequestType { get; set; }
        public string TypeSearch { get; set; }
        public string RequestSearch { get; set; }
        public string Request {  get; set; }
        public int Value { get; set; }

        public UnitTrend() { }

    }
}
