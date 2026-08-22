"""Backfilling matrikkeli profiles.

Kept out of the migration module so it can be tested directly: the suite
runs with --nomigrations and never executes migrations.
"""


def free_slug(base: str, taken: set[str]) -> str:
    """A slug nobody holds, derived from ``base``.

    ``Person.slug`` is unique, and a legacy row may already hold the value
    a new profile would take, so numbered suffixes are appended the same
    way ``Person.save()`` does.
    """
    slug = base
    counter = 0
    while slug in taken:
        counter += 1
        slug = f"{base}-{counter}"
    return slug


def backfill_profiles(user_model, person_model) -> int:
    """Give every account without a matrikkeli profile one.

    Matches what the post-save signal creates for a new account: member
    type ``None`` and the primary key as the slug. Accounts that already
    have a profile are left exactly as they are, so this can be run again
    over the same rows without changing anything.

    Returns the number of profiles created.
    """
    with_profile = set(
        person_model.objects.exclude(user=None).values_list("user_id", flat=True)
    )
    taken = set(person_model.objects.exclude(slug=None).values_list("slug", flat=True))

    created = 0
    missing = user_model.objects.exclude(pk__in=with_profile).order_by("pk")
    for user_id in missing.values_list("pk", flat=True).iterator():
        slug = free_slug(str(user_id), taken)
        person_model.objects.create(user_id=user_id, member_type=0, slug=slug)
        taken.add(slug)
        created += 1
    return created
