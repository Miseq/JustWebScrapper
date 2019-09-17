import platform

from just_it_webscrapper import JustItWebscrapper

if __name__ == "__main__":
    sys = str(platform.system()).lower()
    just_get_IT = JustItWebscrapper(sys)
    just_get_IT.get_offers()
    just_get_IT.close()
