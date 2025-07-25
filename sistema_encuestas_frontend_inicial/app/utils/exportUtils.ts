import jsPDF from "jspdf";
import "jspdf-autotable";
import * as XLSX from "xlsx";

interface ExportOptions {
  filename: string;
  headers: string[];
  data: any[];
  title?: string;
}

// Exportar a PDF
export const exportToPDF = ({ filename, headers, data, title }: ExportOptions) => {
  const doc = new jsPDF({ orientation: 'landscape' });
  
  // Título
  if (title) {
    doc.setFontSize(18);
    doc.setTextColor(33, 150, 243);
    doc.text(title, 20, 20);
  }
  
  // Fecha
  doc.setFontSize(10);
  doc.setTextColor(100);
  doc.text(`Generado el: ${new Date().toLocaleDateString('es-ES')}`, 20, title ? 30 : 20);
  
  // Tabla
  (doc as any).autoTable({
    startY: title ? 40 : 30,
    head: [headers],
    body: data,
    theme: 'grid',
    headStyles: { fillColor: [59, 130, 246] },
    styles: { fontSize: 8 },
    columnStyles: {
      0: { cellWidth: 'auto' },
      1: { cellWidth: 'auto' },
    }
  });
  
  doc.save(`${filename}.pdf`);
};

// Exportar a Excel
export const exportToExcel = ({ filename, headers, data, title }: ExportOptions) => {
  // Crear un nuevo libro
  const ws = XLSX.utils.aoa_to_sheet([headers, ...data]);
  const wb = XLSX.utils.book_new();
  
  // Agregar hoja con título
  XLSX.utils.book_append_sheet(wb, ws, title || "Datos");
  
  // Guardar archivo
  XLSX.writeFile(wb, `${filename}.xlsx`);
};

// Exportar a CSV
export const exportToCSV = ({ filename, headers, data }: ExportOptions) => {
  // Crear contenido CSV
  const csvContent = [
    headers.join(','),
    ...data.map(row => 
      row.map((cell: any) => {
        // Escapar comillas y envolver en comillas si contiene comas
        const cellStr = String(cell);
        if (cellStr.includes(',') || cellStr.includes('"')) {
          return `"${cellStr.replace(/"/g, '""')}"`;
        }
        return cellStr;
      }).join(',')
    )
  ].join('\n');
  
  // Crear blob y descargar
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${filename}.csv`;
  link.click();
};

// Exportar a JSON
export const exportToJSON = ({ filename, data }: { filename: string; data: any }) => {
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
  return objects.map(obj => 
    columnKeys.map(key => obj[key] || '')
  );
}; 