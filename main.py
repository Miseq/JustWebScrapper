from just_it_webscrapper import JustItWebscrapper

if __name__ == "__main__":
    just_get_IT = JustItWebscrapper()
    html = just_get_IT.get_offers()
    with open('just_file', 'w') as writier:
        writier.write(html)
