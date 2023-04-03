--member의 기본키를 외래키로 가져올 테이블
create table DOG_FIND(
    REQ_NO NUMBER(38,0) not null primary key,
    F_MEM_ID VARCHAR2(15 BYTE) not null,				     	    --외래키로 지정할 컬럼
    popfile varchar2(100),
    happenDt varchar2(8),
    happenPlace varchar2(100),
    kindCd  varchar2(50),
    colorCd varchar2(30),
    age varchar2(30),
    processState varchar2(10),
    sexCd varchar2(1),
    neuterYn varchar2(1),
    specialMark varchar2(200),
    
    CONSTRAINT fk_F_MEM_ID foreign key(F_MEM_ID) references member (MEM_ID)  --외래키 지정문
  --CONSTRAINT [FK명] foreign key([FK가 될 컬럼명]) references [PK가 위치하는 테이블] ([PK컬럼명])
--* 컬럼명은 외래키로 가져오는 기본키의 컬럼명과 동일하게 작성해도 된다.
--* FK명은 다른테이블과 중복이 되서는 안된다. 
);