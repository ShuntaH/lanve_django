from django.views.generic import View
from django.http import JsonResponse

from lanve.models import Favorite


class CreateFavoriteView(View):
    """
    いいね投票作成処理を行う
    """

    def post(self, request, *args, **kwargs):
        res = {
            'result': False,
            'message': '処理に失敗しました。'
        }
        # POST値に'comment_id'がなければBAD REQUESTとする
        if not 'comment_id' in request.POST:
            return JsonResponse(res, status=400)

        # コメントIDとIPアドレスの取得
        comment_id = request.POST['comment_id']
        ip_address = get_client_ip(request)

        # 既にIP登録があればコンフリクト
        if Favorite.objects.filter(comment_id=comment_id, ip_address=ip_address):
            res['message'] = 'favo済みです'
            return JsonResponse(res, status=409)

        # Favoriteの保存に成功した場合のみ成功
        if Favorite.objects.create_favorite(ip_address, comment_id):
            res['result'] = True
            res['message'] = 'added a favorite!!'
            return JsonResponse(res, status=201)
        else:
            return JsonResponse(res, status=500)


def get_client_ip(request):
    """
    IPアドレスを取得する
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class DeleteFavoriteView(View):
    """
    いいね投票作成処理を行う
    """

    def post(self, request, *args, **kwargs):
        res = {
            'result': False,
            'message': '処理に失敗しました。'
        }
        # POST値に'comment_id'がなければBAD REQUESTとする
        if not 'comment_id' in request.POST:
            return JsonResponse(res, status=400)

        # コメントIDとIPアドレスの取得
        comment_id = request.POST['comment_id']
        ip_address = get_client_ip(request)

        # Favoriteの保存に成功した場合のみ成功
        if Favorite.objects.filter(comment_id=comment_id, ip_address=ip_address).delete():
            res['result'] = True
            res['message'] = 'deleted a favorite!!'
            return JsonResponse(res, status=201)
        else:
            return JsonResponse(res, status=500)


def get_client_ip(request):
    """
    IPアドレスを取得する
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
