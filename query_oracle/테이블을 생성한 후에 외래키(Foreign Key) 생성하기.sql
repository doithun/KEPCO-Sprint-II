ALTER TABLE boardA
ADD CONSTRAINT fk_midx foreign KEY(midx) references memberA (midx);
--ALTER TABLE [FK를 생성시킬 테이블명]
--ADD CONSTRAINT [FK명] foreign KEY(FK가 될 컬럼명) references [PK가 위치하는 테이블] ([PK컬럼명]);