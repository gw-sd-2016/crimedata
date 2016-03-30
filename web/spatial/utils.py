from spatial.models import CrimeType


def crime_type_tree(self):
    tree = []
    top_level = CrimeType.objects.filter(parent=None)

    for ct in top_level:
        tree.append({"id": ct.pk, "disp": ct.friendly_name})

        curr_level = 1
        children = CrimeType.objects.filter(parent=ct)
        while children.count() != 0:
            for child in children:
                tree.append({
                    "id": child.pk,
                    "disp": "%s%s" % ("-" * curr_level, child.friendly_name)
                })

            children = CrimeType.objects.filter(parent=child)
            curr_level += 1