import re
import json

digits = {"1":"۱", 
          "2":"۲", 
          "3":"۳", 
          "4":"۴", 
          "5":"۵", 
          "6":"۶", 
          "7":"۷", 
          "8":"۸", 
          "9":"۹", 
          "0":"۰", }

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
        .babintro {
            font-size: 0.9rem;
            font-weight: 600;
        }
        /* Style for words that will have a tooltip */
        .word-tooltip {
            color: #0056b3; /* Blue color */
            text-decoration: underline;
            text-decoration-style: dotted;
            cursor: help; /* Indicates help is available */
            position: relative; /* Needed for potential advanced positioning, though not strictly required here */
        }

        /* The tooltip box */
        #tooltip {
            display: none; /* Hidden by default */
            position: absolute; /* Positioned relative to the viewport or nearest positioned ancestor */
            border: 1px solid #ccc;
            background-color: #fff M50;
            color: #333;
            padding: 8px 12px;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            font-size: 0.9em;
            max-width: 250px; /* Prevent it from getting too wide */
            z-index: 1000; /* Ensure it's on top */
            pointer-events: none; /* IMPORTANT: Prevents the tooltip itself from blocking mouse events */
            background-color: lightyellow; /* Make it visually distinct */
            text-align: right;
            direction: rtl;
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
        </table>
    </div>
    <div id="tooltip"></div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const tooltip = document.getElementById('tooltip');
            const wordsWithTooltips = document.querySelectorAll('.word-tooltip');
            let isTouch = false; // Flag to differentiate touch/mouse slightly if needed

            // Function to show and position the tooltip
            const showTooltip = (event) => {
                const span = event.target;
                const explanation = span.getAttribute('data-explanation');
                if (!explanation) return; // Exit if no explanation text

                tooltip.innerHTML = explanation;
                tooltip.style.display = 'block'; // Make it visible *before* measuring

                let x, y;
                let eventType = event.type;

                if (eventType.startsWith('touch')) {
                    isTouch = true;
                    // Use the first touch point
                    if (event.touches && event.touches.length > 0) {
                        x = event.touches[0].pageX;
                        y = event.touches[0].pageY;
                    } else {
                        // Fallback if touch coordinates aren't available for some reason
                        x = event.pageX || span.getBoundingClientRect().left + window.scrollX;
                        y = event.pageY || span.getBoundingClientRect().bottom + window.scrollY;
                    }

                } else { // Mouse event
                    isTouch = false;
                    x = event.pageX;
                    y = event.pageY;
                }


                // Add a small offset so the tooltip doesn't sit directly under the cursor/finger
                const offsetX = 10;
                const offsetY = 15;

                let tooltipX = x + offsetX;
                let tooltipY = y + offsetY;

                // --- Boundary Checks ---
                // Wait a fraction of a second for the browser to render the tooltip
                // This helps get accurate dimensions, especially if content changes
                requestAnimationFrame(() => {
                    // Check right boundary
                    if (tooltipX + tooltip.offsetWidth > window.innerWidth) {
                        tooltipX = window.innerWidth - tooltip.offsetWidth - 10; // Position left of boundary
                        // If near cursor, maybe shift left from cursor instead
                        if (tooltipX > x - tooltip.offsetWidth - offsetX) {
                            tooltipX = x - tooltip.offsetWidth - offsetX;
                        }
                    }
                    // Check left boundary (less common case with default offset)
                    if (tooltipX < 0) {
                        tooltipX = 10;
                    }

                    // Check bottom boundary
                    if (tooltipY + tooltip.offsetHeight > window.innerHeight + window.scrollY ) {
                        // If it overflows below, position it above the cursor/touch point
                        tooltipY = y - tooltip.offsetHeight - 10;
                    }
                    // Check top boundary (less common case with default offset)
                    if (tooltipY < window.scrollY) {
                        tooltipY = window.scrollY + 10; // Keep it within viewport top
                    }


                    tooltip.style.left = `${tooltipX}px`;
                    tooltip.style.top = `${tooltipY}px`;
                });
            };

            // Function to hide the tooltip
            const hideTooltip = () => {
                // Optionally add a small delay for touch to prevent immediate hiding if user slightly moves finger
                // if (isTouch) {
                //     setTimeout(() => { tooltip.style.display = 'none'; }, 100);
                // } else {
                    tooltip.style.display = 'none';
                // }
            };

            // Add event listeners to each word
            wordsWithTooltips.forEach(word => {
                // Mouse events
                word.addEventListener('mouseover', showTooltip);
                word.addEventListener('mouseout', hideTooltip);

                // Touch events
                // 'touchstart' reliably triggers on tap
                word.addEventListener('touchstart', (e) => {
                    // e.preventDefault(); // Prevent potential scrolling ONLY if tap is solely for tooltip
                    showTooltip(e);
                });
                // Note: 'mouseout' often fires after a touchend/tap on many devices,
                // so it helps hide the tooltip. If issues arise, you might need
                // to add a global 'touchstart' listener on the body to hide
                // the tooltip when tapping elsewhere.
                // word.addEventListener('touchend', hideTooltip); // Could also explicitly hide here
            });

            // Optional: Hide tooltip if user scrolls
            // window.addEventListener('scroll', hideTooltip, { passive: true });

        });
    </script>
</body>
</html>
"""

with open("tooltips.json", "r") as file:
    tooltipData = json.load(file)

def tooltip(token):
    try:
        return tooltipData[token]
    except KeyError:
        return "بو سؤزجۆگۆن نه آنلاما گلدیگینی بورایا اکله‌یه‌جگم!"


def addTooltip(text):
    withTooltip = ""
    for token in text.split():
        if len(token) < 2:
            withTooltip += f"{token} "
        else:
            withTooltip += f"<span class=\"word-tooltip\" data-explanation=\"{tooltip(token)}\">{token}</span> "
    return withTooltip


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
                        {addTooltip(mergedLines[2 * (i + 1) + 1])}
                        <br/>
                        {addTooltip(mergedLines[2 * (i + 2) + 1])}
                    </td>
                </tr>"""
            i += 3
        elif mergedLines[2 * i + 0][:3] == "bâb":
            bab = ""
            for digit in str(int(mergedLines[2 * i + 0][4:-1])):
                bab += digits[digit]
            mergedHtml += f"""
            <tr>
                <td class="ltr babintro babnumber"></td>
                <td class="rtl babintro babnumber">{mergedLines[2 * (i + 0) + 1]} {bab}</td>
            </tr>
            <tr>
                <td class="ltr babintro">{mergedLines[2 * (i + 1) + 0]}</td>
                <td class="rtl babintro">{addTooltip(mergedLines[2 * (i + 1) + 1])}</td>
            </tr>"""
            i += 2
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
                        {addTooltip(mergedLines[2 * (i + 1) + 1])}
                    </td>
                </tr>"""
            i += 2
        else:
            mergedHtml += f"""
                <tr>
                    <td class="ltr">{mergedLines[2 * i + 0]}</td>
                    <td class="rtl">{addTooltip(mergedLines[2 * i + 1])}</td>
                </tr>"""
            i += 1


    htmlFile = open("../Text/merged.html", "w")
    htmlFile.write(htmlTop + mergedHtml + htmlBottom)
    htmlFile.close()






