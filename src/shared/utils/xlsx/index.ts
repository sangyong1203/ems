import Excel from '@/shared/utils/xlsx/Excel.module.js'
import dayjs from 'dayjs'


export const makeExcelAndDownload = (downloadData:any[], title:string, tableHeaders: string[], fileName: string) => {

    // --------------sheet style ---------------------
    const columStyle = {
        height: 24,
        width: 1,
    }
    const titleStyle = {
        verticalAlign: 'middle',
        textAlign: 'center',
        backgroundColor: '#c1daf2',
        fontSize: 18,
        fontWeight: 'bold',
        border: '1px solid #000000',
        height: 24,
    }
    const tableHeader = {
        textAlign: 'center',
        border: '1px solid #000000',
        verticalAlign: 'middle',
        backgroundColor: '#f1f1f1',
        fontWeight: 'bold',
        fontSize: 10,
    }
    const indexNumber = {
        textAlign: 'center',
        border: '1px solid #000000',
        verticalAlign: 'middle',
        fontSize: 10,
        width: 30
    }
    const tableListStyle = {
        textAlign: 'center',
        border: '1px solid #000000',
        verticalAlign: 'middle',
        fontSize: 10,
        width: 140,
        height: 24,
    }
    //-------------------------------------


    const tableHeaderList:any = []
    makeHeaderRow(tableHeaders)
    function makeHeaderRow(headers: string[]){
        tableHeaderList.push({
            text: 'NO',
            style: Object.assign({},tableHeader, {width:20}),
        })
        headers.forEach(name => {
            const item =  {
                text: name,
                style: Object.assign({},tableHeader),
            }
            tableHeaderList.push(item)
        })
    } 

    const sheet1 = {
        name: 'Sheet1',
        data: [ tableHeaderList ],
    }

    if(title){
        sheet1.data.unshift([{ style: columStyle }])
        sheet1.data.unshift(
            [
                {
                    text: title,
                    colspan: tableHeaderList.length,
                    rowspan: 2,
                    style: Object.assign({},titleStyle),
                },
                { style: columStyle }
            ]
        )
    }

    for (let i = 0; i < downloadData.length; i++) {
            const keys = Object.keys(downloadData[i])
            const row = []
            
            row.push({
                text: i + 1,
                style: Object.assign({},indexNumber),
            })
            keys.forEach( keyName => {
                const item = {
                    text: downloadData[i][keyName],
                    style: Object.assign({},tableListStyle),
                }
                row.push(item)
            } )
            
            sheet1.data.push(row)
    }

    Excel.make([sheet1], (fileName??('downloadExcel'+ dayjs(new Date()).format('YYYY-MM-DD'))) )
}
