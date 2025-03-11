import requests
from bs4 import BeautifulSoup
import xlsxwriter

page = requests.get(
    "https://www.digitalocean.com/community/tutorials/linux-commands#the-dd-command-in-linux"
)
Linux_table = []


def main(page):
    if page.status_code == 200:
        src = page.content
        soup = BeautifulSoup(src, "lxml")
        Linux_page = soup.find("div", {"class": "faSfKY"})

        if Linux_page:
            Linux_tittle = Linux_page.find("h3").text.strip()
            Linux_command = Linux_page.find("ol").find_all("li")

            if Linux_command:
                for command in Linux_command:
                    link_tag = command.find("a")
                    if link_tag:
                        strong_text = link_tag.find("strong").get_text(strip=True)
                        remaining_text = link_tag.get_text(strip=True).replace(
                            strong_text, ""
                        )

                        # جمع الصور أو الروابط مع الوصف
                        img_tag = command.find("img")
                        img_src = img_tag["src"] if img_tag else ""

                        full_description = remaining_text
                        if img_src:
                            full_description += f" [Image: {img_src}]"

                        Linux_table.append(
                            {
                                "Command": strong_text,
                                "Description": full_description,
                            }
                        )
                    else:
                        print("No link tag found")
            else:
                print("No li or ol elements found")

        else:
            print("لم يتم العثور على العنصر المطلوب داخل الصفحة.")
    else:
        print(f"Failed to retrieve the page. Status code: {page.status_code}")


main(page)

workbook = xlsxwriter.Workbook("Linux_Commands.xlsx")
worksheet = workbook.add_worksheet()

# كتابة رؤوس الأعمدة
headers = Linux_table[0].keys()
for col_num, header in enumerate(headers):
    worksheet.write(0, col_num, header)

# كتابة البيانات
for row_num, data in enumerate(Linux_table, 1):
    for col_num, (key, value) in enumerate(data.items()):
        worksheet.write(row_num, col_num, value)

# حفظ الملف
workbook.close()
