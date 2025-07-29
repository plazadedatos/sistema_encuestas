import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import * as ExcelJS from 'exceljs';

// Función para exportar a PDF
export const exportToPDF = async (
  filename: string,
  headers: string[],
  data: any[],
  title?: string
) => {
  const doc = new jsPDF();

  // Agregar título si se proporciona
  if (title) {
    doc.setFontSize(16);
    doc.text(title, 20, 20);
    doc.setFontSize(10);
    doc.text(
      `Generado el: ${new Date().toLocaleDateString('es-ES')}`,
      20,
      title ? 30 : 20
    );
  }

  // Configurar tabla
  autoTable(doc, {
    head: [headers],
    body: data.map(row => headers.map(header => row[header] || '')),
    startY: title ? 40 : 20,
    styles: {
      fontSize: 8,
      cellPadding: 2,
    },
    headStyles: {
      fillColor: [59, 130, 246],
      textColor: 255,
      fontStyle: 'bold',
    },
  });

  doc.save(`${filename}.pdf`);
};

// Función para exportar a Excel usando ExcelJS
export const exportToExcel = async (
  filename: string,
  headers: string[],
  data: any[],
  title?: string
) => {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('Datos');

  // Agregar título si se proporciona
  if (title) {
    worksheet.addRow([title]);
    worksheet.addRow([
      `Generado el: ${new Date().toLocaleDateString('es-ES')}`,
    ]);
    worksheet.addRow([]); // Línea en blanco
  }

  // Agregar encabezados
  worksheet.addRow(headers);

  // Agregar datos
  data.forEach(row => {
    const rowData = headers.map(header => row[header] || '');
    worksheet.addRow(rowData);
  });

  // Estilizar encabezados
  const headerRow = worksheet.getRow(title ? 4 : 1);
  headerRow.font = { bold: true };
  headerRow.fill = {
    type: 'pattern',
    pattern: 'solid',
    fgColor: { argb: 'FF3B82F6' },
  };
  headerRow.font = { bold: true, color: { argb: 'FFFFFFFF' } };

  // Autoajustar columnas
  worksheet.columns.forEach(column => {
    column.width = 15;
  });

  // Generar archivo
  const buffer = await workbook.xlsx.writeBuffer();
  const blob = new Blob([buffer], {
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${filename}.xlsx`;
  link.click();
  window.URL.revokeObjectURL(url);
};

// Función para exportar a CSV
export const exportToCSV = async ({
  filename,
  data,
}: {
  filename: string;
  data: any[];
}) => {
  if (data.length === 0) return;

  const columnKeys = Object.keys(data[0]);
  const csvContent =
    'data:text/csv;charset=utf-8,' +
    columnKeys.join(',') +
    '\n' +
    data
      .map(obj => columnKeys.map(key => `"${obj[key] || ''}"`).join(','))
      .join('\n');

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement('a');
  link.setAttribute('href', encodedUri);
  link.setAttribute('download', `${filename}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// Exportar a JSON
export const exportToJSON = ({
  filename,
  data,
}: {
  filename: string;
  data: any;
}) => {
  const jsonStr = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonStr], { type: 'application/json' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${filename}.json`;
  link.click();
};

// Función auxiliar para convertir objetos a arrays para la tabla
export const objectsToTableData = (
  objects: any[],
  columnKeys: string[]
): any[][] => {
  return objects.map(obj => columnKeys.map(key => obj[key] || ''));
};
