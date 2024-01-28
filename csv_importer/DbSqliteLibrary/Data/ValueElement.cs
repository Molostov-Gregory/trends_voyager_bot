using CSV_import.Data;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DbSqliteLibrary.Data
{
    /// <summary>
    /// Структура, которая используется для вывода значений
    /// </summary>
    public class ValueElement
    {
        public DateTime Date { get; set; } = DateTime.MinValue;
        public string Request { get; set; } = String.Empty;
        public int Value { get; set; }
        public int Place {  get; set; }

        /// <summary>
        /// Текст сообщения изменения места
        /// </summary>
        public string PlaceChange { get; set; }

        /// <summary>
        /// Направление изменения места
        /// </summary>
        public int PlaceTrendChange { get; set; }
    }
}
