from functools import lru_cache


@lru_cache(maxsize=1)
def get_store_details():
    return {
        "site_logo": '',
        'site_name': 'متجري',
        'headline': 'تسوق بسهولة',
        'address': 'الجزائر',
        'phone_number': '0555000000',
        'email': 'store@example.com',
        'about_text': 'متجر إلكتروني جزائري.',
        'facebook_url': '#',
        'instagram_url': '#',
        'primary_color': '#0f172a',
        'primary_dark': '#0b1120',
        'primary_light': '#1e293b',
        'accent_color': '#f97316',
        'accent_light': '#fb923c',
        'accent_bg': '#fff7ed',
        'secondary_color': '#2563eb',
        'secondary_light': '#3b82f6',
        'secondary_bg': '#eef2ff',
        'success_color': '#10b981',
        'success_bg': '#ecfdf5',
        'accent_rgb': '249 115 22',
    }


def site_data(request):
    return get_store_details()
