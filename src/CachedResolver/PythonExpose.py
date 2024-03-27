import inspect
import logging
import os
from functools import wraps

from pxr import Ar

try:
    from pipe23.usd.resolver import Resolver, ResolverContext
    
except:
    print("*********Warning the custom Usd Asset Resolver could not be imported, creating a dummy one.")
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
            resolved_asset_path = assetPath
            print("**********Dummy Caching for resolved asset: \n\t{0} ---> {1}".format(assetPath, resolved_asset_path))
            context.AddCachingPair(assetPath, resolved_asset_path)
            return resolved_asset_path
