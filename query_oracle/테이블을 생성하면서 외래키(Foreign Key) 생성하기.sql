--member�� �⺻Ű�� �ܷ�Ű�� ������ ���̺�
create table DOG_FIND(
    REQ_NO NUMBER(38,0) not null primary key,
    F_MEM_ID VARCHAR2(15 BYTE) not null,				     	    --�ܷ�Ű�� ������ �÷�
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
    
    CONSTRAINT fk_F_MEM_ID foreign key(F_MEM_ID) references member (MEM_ID)  --�ܷ�Ű ������
  --CONSTRAINT [FK��] foreign key([FK�� �� �÷���]) references [PK�� ��ġ�ϴ� ���̺�] ([PK�÷���])
--* �÷����� �ܷ�Ű�� �������� �⺻Ű�� �÷���� �����ϰ� �ۼ��ص� �ȴ�.
--* FK���� �ٸ����̺�� �ߺ��� �Ǽ��� �ȵȴ�. 
);