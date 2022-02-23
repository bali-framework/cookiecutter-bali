import time

from conf import redis_cli, settings

__all__ = ["set_otp", "check_otp"]
TTL = 5 * 60


def get_redis_key(phone_number):
    return f"{settings.TITLE}:{phone_number}:OTP"


def get_score():
    return int(time.time())


def set_otp(phone_number, otp):
    redis_key, score = get_redis_key(phone_number), get_score()
    with redis_cli.pipeline() as pipeline:
        pipeline.zremrangebyscore(redis_key, 0, score - TTL)
        pipeline.zadd(redis_key, {otp: score})
        pipeline.expire(redis_key, TTL)
        pipeline.execute()


def check_otp(phone_number, otp):
    redis_key, score = get_redis_key(phone_number), get_score()
    redis_cli.zremrangebyscore(redis_key, 0, score - TTL)
    return redis_cli.zrank(redis_key, otp) is not None
