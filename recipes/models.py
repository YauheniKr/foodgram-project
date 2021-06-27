from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.shortcuts import reverse

User = get_user_model()


class Unit(models.Model):
    dimension = models.CharField(max_length=20,
                                 verbose_name='единица измерения')

    class Meta:
        verbose_name = 'единица измерения'
        verbose_name_plural = 'единицы измерения'

    def __str__(self):
        return self.dimension


class Ingredient(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='название ингредиента')
    unit = models.ForeignKey(Unit, verbose_name='единица измерения',
                             related_name='ingredients',
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')
    created = models.DateTimeField('Дата публикации', auto_now_add=True,
                                   db_index=True
                                   )
    title = models.CharField(max_length=200, verbose_name='Название рецепта')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True,
                              verbose_name='Картинка рецепта')
    text = models.TextField(verbose_name='Изображение блюда')
    slug = AutoSlugField(populate_from='title', allow_unicode=True)
    cooking_time = models.DurationField(verbose_name='Время приготовления')
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ингредиенты рецепта',
                                         through='RecipeIngredient')
    tags = models.ManyToManyField('Tag', related_name='recipes',
                                  verbose_name='Метки рецепта')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('index')


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, verbose_name='ингредиент',
                                   on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, verbose_name='рецепт',
        on_delete=models.CASCADE,
        related_name='ingredients_amounts'
    )
    quantity = models.DecimalField(
        max_digits=6, verbose_name='количество',
        decimal_places=1,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_recipe_ingredient'
            )
        ]


class Tag(models.Model):
    title = models.CharField('Имя тега', max_length=50, db_index=True)
    display_name = models.CharField('Имя тега для шаблона', max_length=50)
    color = models.CharField('Цвет тега', max_length=50)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Пользователь')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite_by',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            )
        ]


class Purchase(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchase_by',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_purchase'
            )
        ]
