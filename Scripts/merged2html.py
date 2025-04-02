import re

htmlTop = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Representation</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh; /* Allow scrolling if content exceeds viewport height */
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #E8F5E9;
            overflow-y: auto; /* Ensure vertical scrolling */
        }
        h1 {
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .table-container {
            width: 50%;
            min-width: 500px;
            background-color: #ffffff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 20px;
            border-collapse: collapse;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px 10px; /* Add padding to create distance from the borders */
            text-align: left;
            border-bottom: 2px solid #444;
        }
        th {
            background-color: #A5D6A7; 
        }
        td {
            background-color: #C8E6C9;
        }
        .rtl {
            text-align: right;
            direction: rtl;
        }
        .ltr {
            text-align: left;
            direction: ltr;
        }
        .beytnumber {
            border-bottom: 0;
        }
        .babnumber {
            border-bottom: 0;
        }
        .bab {
            font-size: 1.0rem;
            font-weight: 800;
        }
    </style>
</head>
<body>
    <h1>بسم الله الرحمن الرحیم</h1>
    <div class="table-container">
        <table>
            <tr>
                <th class="ltr">Kutadğu Bilig</th>
                <th class="rtl">قوتادغو بیلیگ</th>
            </tr>
"""

htmlBottom = """
            <tr>
                <td class="ltr">This is a long text line in the left column to help debug the code properly. This line should align with the right column line.</td>
                <td class="rtl">هذا هو نص طويل في العمود الأيمن للمساعدة في تصحيح الكود بشكل صحيح. يجب أن تتماشى هذه السطر مع السطر في العمود الأيسر.</td>
            </tr>
            <tr>
                <td class="ltr">Another long text line in the left column to ensure proper alignment with the right column. Debugging is easier with longer texts.</td>
                <td class="rtl">نص طويل آخر في العمود الأيمن لضمان المحاذاة الصحيحة مع العمود الأيسر. يكون التصحيح أسهل مع النصوص الأطول.</td>
            </tr>
            <tr>
                <td class="ltr">Yet another long text line in the left column to test out the alignment and spacing between the two columns.</td>
                <td class="rtl">نص طويل آخر في العمود الأيمن لاختبار المحاذاة والمسافة بين العمودين.</td>
            </tr>
        </table>
    </div>
</body>
</html>
"""





if __name__ == "__main__":
    mergedLines = []
    mergedFile = open("../Text/merged.txt", "r")
    for line in mergedFile:
        mergedLines.append(line.strip())
    mergedFile.close()

    mergedHtml = ""
    i = 0
    while i < len(mergedLines) // 2:
        if mergedLines[2 * i + 0][:4] == "beyt":
            mergedHtml += f"""
                <tr>
                    <td class="ltr beytnumber"></td>
                    <td class="rtl beytnumber">{mergedLines[2 * (i + 0) + 1]}</td>
                </tr>
                <tr>
                    <td class="ltr">
                        {mergedLines[2 * (i + 1) + 0]}
                        <br/>
                        {mergedLines[2 * (i + 2) + 0]}
                    </td>
                    <td class="rtl">
                        {mergedLines[2 * (i + 1) + 1]}
                        <br/>
                        {mergedLines[2 * (i + 2) + 1]}
                    </td>
                </tr>"""
            i += 3
        elif re.fullmatch(r"^[\d]+$", mergedLines[2 * i + 0]):
            mergedHtml += f"""
                <tr>
                    <td class="ltr bab babnumber"></td>
                    <td class="rtl bab babnumber">{mergedLines[2 * (i + 0) + 1]}</td>
                </tr>
                <tr>
                    <td class="ltr bab">
                        {mergedLines[2 * (i + 1) + 0]}
                    </td>
                    <td class="rtl bab">
                        {mergedLines[2 * (i + 1) + 1]}
                    </td>
                </tr>"""
            i += 2
        else:
            mergedHtml += f"""
                <tr>
                    <td class="ltr">{mergedLines[2 * i + 0]}</td>
                    <td class="rtl">{mergedLines[2 * i + 1]}</td>
                </tr>"""
            i += 1


    htmlFile = open("../Text/merged.html", "w")
    htmlFile.write(htmlTop + mergedHtml + htmlBottom)
    htmlFile.close()






