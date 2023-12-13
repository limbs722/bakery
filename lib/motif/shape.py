from bakery.lib.motif import Fixture

class ResponseCode( Fixture ): pass

'''
    0 + xxx => 성공관련 코드
    
    3 + xxx => 인증관련 코드
'''

ResponseCode.fix( lambda t: t, (
    ( 'SUCCESS',            ('0000', '성공') ),
    ( 'SUCCESS_CREATED',    ('0001', '생성' )),
    ( 'SUCCESS_ACCEPTED',   ('0002', '수락' )),
    ( 'SUCCESS_DELETE',     ('0003', '삭제' )),
    ( 'SUCCESS_UPDATE',     ('0004', '갱신' )),
    ( 'UNAUTHORIZED',       ('3000', '로그인에 실패했습니다.') ),
    ( 'NO_EXTERNAL_TOKEN',  ('3001', '관련된 유효한 외부 토큰이 없습니다' )),
    ( 'INVALID_TOKEN',      ('3002', '부적절한 토큰입니다.' )),
    ( 'EXPIRED_TOKEN',      ('3003', '만료된 토큰입니다.' )),
    ( 'FAIL',               ('9999', '오류' ))
))    

def Response( code, data, **args ):
    return dict( code = code[ 0 ], data = data, msg= code[ 1 ],  **args )
