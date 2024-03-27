import inspect
import logging
import os
from functools import wraps

from pxr import Ar
import ftrack_api


def ftrack_resolve(identifier):
    
    tokens = identifier.split("/")
    project_name = tokens[0]
    asset_name = tokens[1]
    try:
        version = int(tokens[-1].lstrip("v"))
    except ValueError:
        version = tokens[-1]
        
    session = ftrack_api.Session(server_url=os.environ["SHIFT_FT_URL"],
                                 api_key=os.environ["SHIFT_FT_KEY"],
                                 api_user=os.environ["SHIFT_FT_USER"],
                                 plugin_paths=[os.environ["SHIFT_FT_PLUGIN_PATH"]])
    
    project_entity = session.query('select id from Project where name is {0}'.format(project_name)).first()
    asset_entity = session.query('select id, latest_version from Asset where project_id is {0} and name is {1}'.format(project_entity['id'], asset_name)).first()
    if isinstance(version, int):
        version_entity = session.query('select components from AssetVersion where asset_id is {0} and version is {1}'.format(asset_entity['id'], version)).first()
    elif version=='latest':
        del(asset_entity['latest_version'])
        session.populate(asset_entity, 'latest_version')
        version_entity = asset_entity['latest_version']
    
    #Get the component path
    location = session.pick_location()
    component = version_entity['components'][0]
    
    return location.get_filesystem_path(component), version!='latest'
    

class Resolver:

    @staticmethod
    def CreateRelativePathIdentifier(resolver, anchoredAssetPath, assetPath, anchorAssetPath):
        """Returns an identifier for the asset specified by assetPath and anchor asset path.
        It is very important that the anchoredAssetPath is used as the cache key, as this
        is what is used in C++ to do the cache lookup.

        We have two options how to return relative identifiers:
        - Make it absolute: Simply return the anchoredAssetPath. This means the relative identifier
                            will not be passed through to ResolverContext.ResolveAndCache.
        - Make it non file based: Make sure the remapped identifier does not start with "/", "./" or"../"
                                  by putting some sort of prefix in front of it. The path will then be
                                  passed through to ResolverContext.ResolveAndCache, where you need to re-construct
                                  it to an absolute path of your liking. Make sure you don't use a "<somePrefix>:" syntax,
                                  to avoid mixups with URI based resolvers.

        Args:
            resolver (CachedResolver): The resolver
            anchoredAssetPath (str): The anchored asset path, this has to be used as the cached key.
            assetPath (str): An unresolved asset path.
            anchorAssetPath (Ar.ResolvedPath): A resolved anchor path.

        Returns:
            str: The identifier.
        """
        LOG.debug("::: Resolver.CreateRelativePathIdentifier | {} | {} | {}".format(anchoredAssetPath, assetPath, anchorAssetPath))
        return


class ResolverContext:

    @staticmethod
    def Initialize(context):
        """Initialize the context. This get's called on default and post mapping file path
        context creation.

        Here you can inject data by batch calling context.AddCachingPair(assetPath, resolvePath),
        this will then populate the internal C++ resolve cache and all resolves calls
        to those assetPaths will not invoke Python and instead use the cache.

        Args:
            context (CachedResolverContext): The active context.
        """
        LOG.debug("::: ResolverContext.Initialize")
        return

    @staticmethod
    def ResolveAndCache(context, assetPath):
        """Return the resolved path for the given assetPath or an empty
        ArResolvedPath if no asset exists at that path.
        Args:
            context (CachedResolverContext): The active context.
            assetPath (str): An unresolved asset path.
        Returns:
            str: The resolved path string. If it points to a non-existent file,
                 it will be resolved to an empty ArResolvedPath internally, but will
                 still count as a cache hit and be stored inside the cachedPairs dict.
        """
        LOG.debug(
            "::: ResolverContext.ResolveAndCache | {} | {}".format(assetPath, context.GetCachingPairs())
        )
        resolved_asset_path, toCache = ftrack_resolve(assetPath)
        print("**********Resolved asset: \n\t{0} ---> {1}".format(assetPath, resolved_asset_path))
        if toCache:
            context.AddCachingPair(assetPath, resolved_asset_path)
        return resolved_asset_path
