from django.db import migrations, models


def forwards_func(apps, schema_editor):
    from posts.models import calculate_excerpt_from_markdown

    Post = apps.get_model("posts", "Post")
    for post in Post.objects.all():
        post.excerpt = calculate_excerpt_from_markdown(post.body)
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0003_auto_20180304_2236"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="excerpt",
            field=models.CharField(default="", max_length=140),
            preserve_default=False,
        ),
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
    ]
