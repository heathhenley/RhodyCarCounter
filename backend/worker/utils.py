import requests
import bs4


BASE_URL = "https://www.dot.ri.gov"
CAM_LIST_URL = f"{BASE_URL}/travel/cameras_metro.php"


# scrape cam link and name from pvd traffic site, returns a list of dicts with
# the cam data (name, id, link, description from alt text)
def get_cams_from_page(url=CAM_LIST_URL):
  try:
    res = requests.get(url, timeout=1)
  except Exception as e:
    print('f{e}')
    return None
  if res.status_code != 200:
    return None
  cameras = []
  soup = bs4.BeautifulSoup(res.content, "html.parser")
  section = soup.find("div", attrs={"class": "section-container"})
  for list_item in section.find_all("li"):
    a_tag = list_item.a
    if not a_tag:
      continue
    cam_relative_link = a_tag.attrs['href']
    cam_link = f"{BASE_URL}/{cam_relative_link.replace('../', '')}"
    cam_id = a_tag.img.attrs['id']
    cam_description = a_tag.img.attrs['alt']
    cam_name = list_item.text
    cameras.append(dict(id=cam_id,
                        name=cam_name,
                        description=cam_description,
                        link=cam_link))
  return cameras

if __name__ == "__main__":
  cams = get_cams_from_page(CAM_LIST_URL)
  print(cams)
  print(f"Cam count: {len(cams)}")
  