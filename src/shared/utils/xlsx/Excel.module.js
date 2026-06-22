/* eslint-disable no-empty */
/************************************************
 * Excel.module.js
 * Created at 2021. 8. 25. 오후 2:59:40.
 *
 * @author soohongkim
 ************************************************/

/** style
  color?: CSSStyleDeclaration["color"],
  background?: CSSStyleDeclaration["background"],
  backgroundColor?: CSSStyleDeclaration["backgroundColor"],
  textAlign?: CSSStyleDeclaration["textAlign"],
  border?: CSSStyleDeclaration["border"],
  borderTop?: CSSStyleDeclaration["borderTop"],
  borderRight?: CSSStyleDeclaration["borderRight"],
  borderLeft?: CSSStyleDeclaration["borderLeft"],
  borderBottom?: CSSStyleDeclaration["borderBottom"],
  verticalAlign?: CSSStyleDeclaration["verticalAlign"],
  width?: number | 'auto',
  height?: number | 'auto',
  fontSize?: number,
  fontWeight?: 'normal' | 'bold',
  whiteSpace: 'nowrap' | 'normal'
*/

let src = import("src/shared/utils/xlsx/XLSX.min.js")
let script = document.createElement("script")
script.contains = src
document.head.appendChild(script)
let Excel = {}
Excel.make = function (sheetArr, fileName) {
    // eslint-disable-next-line no-undef
    let wb = XLSX.utils.book_new()
    wb.Props = {
        Title: fileName,
        Subject: fileName,
        Author: "Dev.monter",
        CreatedDate: new Date(),
    }

    let alphabet = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "AA",
        "AB",
        "AC",
        "AD",
        "AE",
        "AF",
        "AG",
        "AH",
        "AI",
        "AJ",
        "AK",
        "AL",
        "AM",
        "AN",
        "AO",
        "AP",
        "AQ",
        "AR",
        "AS",
        "AT",
        "AU",
        "AV",
        "AW",
        "AX",
        "AY",
        "AZ",
    ]

    sheetArr.forEach(function (sheet) {
        //each sheet

        let sheet_width = 0
        let sheet_height = sheet.data.length
        let ws = {}
        let merge_data = []
        sheet.data.forEach(function (row, ri) {
            let cur_ri = ri
            let cur_ci = -1
            row.forEach(function (col) {
                cur_ci++
                for (let mi = 0; mi < merge_data.length; mi++) {
                    let merge = merge_data[mi]
                    if (merge.s.c <= cur_ci && cur_ci <= merge.e.c && merge.s.r <= cur_ri && cur_ri <= merge.e.r) {
                        cur_ci += merge.e.c - cur_ci + 1
                    }
                }
                let cr = alphabet[cur_ci] + String(cur_ri + 1)
                if (!ws[cr]) {
                    ws[cr] = {
                        t: "s",
                        v: col.text || "",
                        s: {
                            alignment: {
                                wrapText: true,
                            },
                        },
                    }
                }

                if (col.img) {
                    if (!ws["!images"]) ws["!images"] = []
                    ws["!images"].push({
                        "!link": col.img.src,
                        "!pos": { c: cur_ci, r: cur_ri, x: col.img.left, y: col.img.top, w: col.img.width, h: col.img.height },
                        "!datatype": "remote",
                    })
                }

                for (let styleKey in col.style) {
                    switch (styleKey) {
                        case "backgroundColor":
                            ws[cr].s["fgColor"] = { rgb: col.style[styleKey].replace("#", "") }
                            break
                        case "border":
                            var border_arr = col.style[styleKey].split(" ")
                            var borderWidth = ""
                            var borderColor = border_arr[2].replace("#", "")
                            if (border_arr[0] === "1px") {
                                borderWidth = "thin"
                            } else if (border_arr[0] === "2px") {
                                borderWidth = "medium"
                            } else {
                                borderWidth = "thick"
                            }
                            col.colspan = col.colspan || 1
                            col.rowspan = col.rowspan || 1
                            for (let x = 0; x < col.colspan; x++) {
                                let index_ci = cur_ci + x
                                let merged_cr = alphabet[index_ci] + String(cur_ri + 1)
                                if (!ws[merged_cr]) ws[merged_cr] = { t: "s", s: {}, v: "undefined" }
                                ws[merged_cr].s["top"] = { style: borderWidth, color: { rgb: borderColor } }
                                ws[merged_cr].s["bottom"] = { style: borderWidth, color: { rgb: borderColor } }
                                ws[merged_cr].s["left"] = { style: borderWidth, color: { rgb: borderColor } }
                                ws[merged_cr].s["right"] = { style: borderWidth, color: { rgb: borderColor } }
                                if (sheet_width < index_ci) sheet_width = index_ci
                                for (let y = 0; y < col.rowspan; y++) {
                                    let index_ri = cur_ri + 1 + y
                                    let merged_cr = alphabet[index_ci] + String(index_ri)
                                    if (!ws[merged_cr]) ws[merged_cr] = { t: "s", s: {}, v: "undefined" }
                                    ws[merged_cr].s["top"] = { style: borderWidth, color: { rgb: borderColor } }
                                    ws[merged_cr].s["bottom"] = { style: borderWidth, color: { rgb: borderColor } }
                                    ws[merged_cr].s["left"] = { style: borderWidth, color: { rgb: borderColor } }
                                    ws[merged_cr].s["right"] = { style: borderWidth, color: { rgb: borderColor } }
                                    if (sheet_height < cur_ri + 1 + y) sheet_height = cur_ri + 1 + y
                                }
                            }
                            break
                        case "borderTop":
                        case "borderLeft":
                        case "borderBottom":
                        case "borderRight":
                            var side = ''
                            if (styleKey === "borderTop") side = "top"
                            else if (styleKey === "borderLeft") side = "left"
                            else if (styleKey === "borderBottom") side = "bottom"
                            else if (styleKey === "borderRight") side = "right"
                            var borderSide_arr = col.style[styleKey].split(" ")
                            var borderSideWidth = ""
                            var borderSideColor = borderSide_arr[2].replace("#", "")
                            if (borderSide_arr[0] === "1px") {
                                borderSideWidth = "thin"
                            } else if (borderSide_arr[0] === "2px") {
                                borderSideWidth = "medium"
                            } else {
                                borderSideWidth = "thick"
                            }
                            ws[cr].s[side] = { style: borderSideWidth, color: { rgb: borderSideColor } }
                            if (styleKey === "borderTop" || styleKey === "borderBottom") {
                                for (let x = 1; x < col.colspan; x++) {
                                    let merged_cr = alphabet[cur_ci + x] + String(cur_ri + 1)
                                    if (!ws[merged_cr]) ws[merged_cr] = { t: "s", s: {}, v: "undefined", z: "General" }
                                    ws[merged_cr].s[side] = { style: borderSideWidth, color: { rgb: borderSideColor } }
                                }
                            }
                            if (styleKey === "borderLeft" || styleKey === "borderRight") {
                                for (let y = 1; y < col.rowspan; y++) {
                                    let merged_cr = alphabet[cur_ci] + String(cur_ri + 1 + y)
                                    if (!ws[merged_cr]) ws[merged_cr] = { t: "s", s: {}, v: "undefined", z: "General" }
                                    ws[merged_cr].s[side] = { style: borderSideWidth, color: { rgb: borderSideColor } }
                                }
                            }
                            break
                        case "textAlign":
                            if (!ws[cr].s["alignment"]) ws[cr].s["alignment"] = {}
                            ws[cr].s["alignment"]["horizontal"] = col.style[styleKey]
                            break
                        case "verticalAlign":
                            if (!ws[cr].s["alignment"]) ws[cr].s["alignment"] = {}
                            switch (col.style[styleKey]) {
                                case "middle":
                                    ws[cr].s["alignment"]["vertical"] = "center"
                                    break
                                default:
                                    ws[cr].s["alignment"]["vertical"] = col.style[styleKey]
                                    break
                            }
                            break
                        case "width":
                            if (!ws["!cols"]) ws["!cols"] = []
                            if (typeof col.style[styleKey] === "number") ws["!cols"][cur_ci] = { wpx: col.style[styleKey] }
                            else if (col.style[styleKey] === "auto") ws["!cols"][cur_ci] = { auto: 1 }
                            break
                        case "height":
                            if (!ws["!rows"]) ws["!rows"] = []
                            if (typeof col.style[styleKey] === "number") ws["!rows"][cur_ri] = { hpx: col.style[styleKey] }
                            else if (col.style[styleKey] === "auto") ws["!rows"][cur_ri] = { auto: 1 }
                            break
                        case "fontSize":
                            ws[cr].s.sz = col.style[styleKey]
                            break
                        case "fontWeight":
                            if (col.style[styleKey] === "bold") {
                                ws[cr].s.bold = 1
                            } else {
                            }
                            break
                        case "whiteSpace":
                            if (col.style[styleKey] === "nowrap") {
                                ws[cr].s.alignment.wrapText = false
                            }
                            break
                    }
                }
                if (col.colspan > 1 || col.rowspan > 1) {
                    let s = { c: cur_ci, r: cur_ri }
                    let e = {
                        c: col.colspan ? cur_ci + col.colspan - 1 : cur_ci,
                        r: col.rowspan ? cur_ri + col.rowspan - 1 : cur_ri,
                    }
                    merge_data.push({ s, e })
                }
            })
            if (sheet_width < cur_ci) sheet_width = cur_ci
        })
        let ref = `A1:${alphabet[sheet_width]}${sheet_height}`
        ws["!ref"] = ref
        ws["!merges"] = merge_data
        //console.log(ws);
        wb.SheetNames.push(sheet.name)
        wb.Sheets[sheet.name] = ws
    })
    // eslint-disable-next-line no-undef
    XLSX.writeFile(wb, fileName + ".xlsx", { cellStyles: true, bookImages: true, bookSST: false })
}

export default Excel
