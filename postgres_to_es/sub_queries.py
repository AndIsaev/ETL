big_request = """array_agg(distinct g.name) as genre,
            array_agg(distinct p.full_name) filter (WHERE pfw.role = 'director') as director,
            array_agg(distinct p.full_name) filter (where pfw.role = 'actor') as actors_names,
            array_agg(distinct p.full_name) filter (where pfw.role = 'writer') as writers_names,
            array_agg(distinct jsonb_build_object('id', p.id, 'name', p.full_name)) filter (where pfw.role = 'actor') as actors,
            array_agg(distinct jsonb_build_object('id', p.id, 'name', p.full_name)) filter (where pfw.role = 'writer') as writers"""

load_person_id = f'''select distinct id
                            from content.person
                            group by id
                            '''
