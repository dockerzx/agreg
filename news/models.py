from django.db import models
from django.template.defaultfilters import truncatewords_html
from time import mktime
import datetime, feedparser
import ssl
from news.lib import modules

#Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title

class Feed(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True, help_text="Don't forget to add http:// or https:// to the URL")
    category =  models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    favicon = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check to see if this is a new feed or not
        new_feed = self.pk is None
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        feed_data = feedparser.parse(self.url)

        #print(feed_data.feed.image)
        # Set feed title field if available
        if new_feed:
            if feed_data.feed.title:
                self.title = feed_data.feed.title
            else:
                self.title = "Undefined"

        self.favicon = modules.get_fi_link(self.url)

        super(Feed, self).save(*args, **kwargs)

        if new_feed:
            self.get_feed_articles()

    def get_feed_articles(self):
        feed_data = feedparser.parse(self.url)
        for entry in feed_data.entries:
            try:
                article = Article.objects.get(url=entry.link)
            except:
                article = Article()

            article.title = entry.title
            article.url = entry.link
            article.description = entry.description
            article.description_truncated = truncatewords_html(entry.description, 150)

            # Set publication date
            try:
                published = entry.published_parsed
            except AttributeError:
                try:
                    published = entry.updated_parsed
                except AttributeError:
                    published = entry.created_parsed

            publication_date = datetime.datetime.fromtimestamp(mktime(published))
            date_string = publication_date.strftime('%Y-%m-%d %H:%M:%S')
            article.publication_date = date_string

            article.feed = self
            article.favicon = self.favicon
            article.save()

class Article(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=255)
    url = models.URLField(verbose_name="URL")
    description = models.TextField()
    description_truncated = models.TextField(blank=True, null=True)
    publication_date = models.DateTimeField()
    favicon = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
