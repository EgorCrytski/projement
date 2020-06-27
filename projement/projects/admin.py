from django.contrib import admin

from projects.models import Company, Project, Log, ProjectTag, Tag


class CompaniesListFilter(admin.SimpleListFilter):
    """
    This filter will always return a subset of the instances in a Model, either filtering by the
    user choice or by a default value.
    """
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'specific company'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'specific company'

    default_value = None

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_of_companies = []
        queryset = Company.objects.all()
        for companies in queryset:
            list_of_companies.append(
                (str(companies.id), companies.name)
            )
        return sorted(list_of_companies, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(company_id=self.value())
        return queryset

class CompaniesTagsListFilter(admin.SimpleListFilter):
    """
    This filter will always return a subset of the instances in a Model, either filtering by the
    user choice or by a default value.
    """
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'tag'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'tag'

    default_value = None

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_of_tags = []
        queryset = ProjectTag.objects.all()
        for project_tag in queryset:
            list_of_tags.append(
                (str(project_tag.project.id), project_tag.tag.tagname)
            )
        return sorted(list_of_tags, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(id=self.value())
        return queryset



class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date')
    list_filter = ('company__name', 'company__id', CompaniesListFilter, CompaniesTagsListFilter) #, 'show_tags')
    ordering = ('-start_date',)

    fieldsets = (
        (None, {'fields': ['company', 'title', 'start_date', 'end_date']}),
        ('Estimated hours', {'fields': ['estimated_design', 'estimated_development', 'estimated_testing']}),
        ('Actual hours', {'fields': ['actual_design', 'actual_development', 'actual_testing']}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()

        return 'company',



admin.site.register(Company)
admin.site.register(Log)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectTag)
admin.site.register(Tag)
