BOT_NAME = 'leroy_images'

SPIDER_MODULES = ['leroy_images.spiders']
NEWSPIDER_MODULE = 'leroy_images.spiders'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {'leroy_images.pipelines.LeroyImagesPipeline': 1}
# ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}

FILES_STORE = r'downloaded'

DOWNLOAD_DELAY = 1
